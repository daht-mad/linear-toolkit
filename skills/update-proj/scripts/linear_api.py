#!/usr/bin/env python3
"""
Linear API 헬퍼 스크립트
프로젝트 업데이트 생성을 위한 GraphQL API 호출

사용법:
  python linear_api.py create-update <project_id> <body_file> [--health onTrack|atRisk|offTrack]
  python linear_api.py whoami
  python linear_api.py my-projects
  python linear_api.py project-issues <project_id>
  python linear_api.py active-cycle <team_id>

환경변수:
  LINEAR_API_TOKEN - Linear API 토큰 (필수)
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

def get_token():
    """LINEAR_API_TOKEN 환경변수 또는 .env 파일에서 토큰 로드"""
    token = os.environ.get('LINEAR_API_TOKEN')
    if token:
        return token

    env_paths = [
        Path.cwd() / '.env',
        Path.home() / '.env',
    ]
    for env_path in env_paths:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith('LINEAR_API_TOKEN='):
                    return line.split('=', 1)[1].strip().strip('"\'')

    print("Error: LINEAR_API_TOKEN not found", file=sys.stderr)
    sys.exit(1)

def graphql_request(query: str, variables: dict = None):
    """Linear GraphQL API 호출 (curl 사용)"""
    token = get_token()
    data = {'query': query}
    if variables:
        data['variables'] = variables

    result = subprocess.run(
        [
            'curl', '-s', '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-H', f'Authorization: {token}',
            '-d', json.dumps(data),
            'https://api.linear.app/graphql'
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"curl error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Invalid JSON response: {result.stdout}", file=sys.stderr)
        sys.exit(1)

def cmd_whoami(args):
    """현재 사용자 정보 조회"""
    result = graphql_request('{ viewer { id name email } }')
    if 'errors' in result:
        print(f"Error: {result['errors']}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result['data']['viewer'], indent=2, ensure_ascii=False))

def cmd_my_projects(args):
    """내가 리드인 프로젝트 목록 조회"""
    viewer = graphql_request('{ viewer { id } }')['data']['viewer']

    query = '''
    query($first: Int!) {
      projects(first: $first) {
        nodes {
          id name state
          lead { id name }
          teams { nodes { id name } }
        }
      }
    }
    '''
    result = graphql_request(query, {'first': 100})

    my_projects = [
        p for p in result['data']['projects']['nodes']
        if p.get('lead') and p['lead']['id'] == viewer['id']
        and p['state'] not in ['canceled', 'completed']
    ]

    print(json.dumps(my_projects, indent=2, ensure_ascii=False))

def cmd_project_issues(args):
    """프로젝트 이슈 목록 조회"""
    query = '''
    query($id: String!) {
      project(id: $id) {
        issues(first: 100) {
          nodes {
            id identifier title
            state { name type }
            cycle { id number startsAt endsAt }
            assignee { name }
            description
          }
        }
      }
    }
    '''
    result = graphql_request(query, {'id': args.project_id})
    print(json.dumps(result['data']['project']['issues']['nodes'], indent=2, ensure_ascii=False))

def cmd_active_cycle(args):
    """팀의 활성 Cycle 및 다음 Cycle 조회"""
    query = '''
    query($id: String!) {
      team(id: $id) {
        activeCycle { id number startsAt endsAt }
        cycles(first: 5) {
          nodes { id number startsAt endsAt }
        }
      }
    }
    '''
    result = graphql_request(query, {'id': args.team_id})
    print(json.dumps(result['data']['team'], indent=2, ensure_ascii=False))

def cmd_create_update(args):
    """프로젝트 업데이트 생성"""
    body = Path(args.body_file).read_text(encoding='utf-8')

    query = '''
    mutation($input: ProjectUpdateCreateInput!) {
      projectUpdateCreate(input: $input) {
        success
        projectUpdate { id url }
      }
    }
    '''
    variables = {
        'input': {
            'projectId': args.project_id,
            'body': body,
            'health': args.health
        }
    }

    result = graphql_request(query, variables)

    if result.get('data', {}).get('projectUpdateCreate', {}).get('success'):
        update = result['data']['projectUpdateCreate']['projectUpdate']
        print(f"✅ 업데이트 생성 완료!")
        print(f"URL: {update['url']}")
    else:
        print(f"❌ 업데이트 생성 실패: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Linear API 헬퍼')
    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('whoami', help='현재 사용자 정보')
    subparsers.add_parser('my-projects', help='내가 리드인 프로젝트 목록')

    p = subparsers.add_parser('project-issues', help='프로젝트 이슈 목록')
    p.add_argument('project_id', help='프로젝트 ID')

    p = subparsers.add_parser('active-cycle', help='팀의 활성 Cycle')
    p.add_argument('team_id', help='팀 ID')

    p = subparsers.add_parser('create-update', help='프로젝트 업데이트 생성')
    p.add_argument('project_id', help='프로젝트 ID')
    p.add_argument('body_file', help='업데이트 내용 마크다운 파일')
    p.add_argument('--health', choices=['onTrack', 'atRisk', 'offTrack'],
                   default='onTrack', help='프로젝트 상태')

    args = parser.parse_args()

    commands = {
        'whoami': cmd_whoami,
        'my-projects': cmd_my_projects,
        'project-issues': cmd_project_issues,
        'active-cycle': cmd_active_cycle,
        'create-update': cmd_create_update,
    }

    commands[args.command](args)

if __name__ == '__main__':
    main()

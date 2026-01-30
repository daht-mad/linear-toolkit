#!/usr/bin/env python3
"""
Linear API 헬퍼 스크립트 - Initiative Update용
이니셔티브 업데이트 생성을 위한 GraphQL API 호출

사용법:
  python linear_api.py whoami
  python linear_api.py my-initiatives
  python linear_api.py initiative-projects <initiative_id>
  python linear_api.py project-updates <project_id> [--limit N]
  python linear_api.py create-initiative-update <initiative_id> <body_file> [--health onTrack|atRisk|offTrack]

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

def cmd_my_initiatives(args):
    """내가 owner인 이니셔티브 목록 조회"""
    viewer = graphql_request('{ viewer { id } }')['data']['viewer']

    query = '''
    query($first: Int!) {
      initiatives(first: $first) {
        nodes {
          id
          name
          description
          status
          targetDate
          owner { id name }
        }
      }
    }
    '''
    result = graphql_request(query, {'first': 50})

    if 'errors' in result:
        print(f"Error: {result['errors']}", file=sys.stderr)
        sys.exit(1)

    # 내가 owner이고 활성 상태인 이니셔티브만 필터링
    # Linear API 상태값: Active, Planned, Paused, Completed
    my_initiatives = [
        i for i in result['data']['initiatives']['nodes']
        if i.get('owner') and i['owner']['id'] == viewer['id']
        and i.get('status') in ['Active', 'Planned']  # 활성 상태만
    ]

    print(json.dumps(my_initiatives, indent=2, ensure_ascii=False))

def cmd_initiative_projects(args):
    """이니셔티브에 연결된 프로젝트 목록 조회"""
    query = '''
    query($id: String!) {
      initiative(id: $id) {
        id
        name
        status
        projects {
          nodes {
            id
            name
            state
            health
            lead { id name }
            teams { nodes { id name } }
          }
        }
      }
    }
    '''
    result = graphql_request(query, {'id': args.initiative_id})

    if 'errors' in result:
        print(f"Error: {result['errors']}", file=sys.stderr)
        sys.exit(1)

    initiative = result['data']['initiative']
    if not initiative:
        print(f"Error: Initiative not found: {args.initiative_id}", file=sys.stderr)
        sys.exit(1)

    # 활성 상태 프로젝트만 필터링 (started, planned)
    active_projects = [
        p for p in initiative['projects']['nodes']
        if p['state'] not in ['canceled', 'completed', 'paused']
    ]

    output = {
        'initiative': {
            'id': initiative['id'],
            'name': initiative['name'],
            'status': initiative['status']
        },
        'projects': active_projects
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

def cmd_project_updates(args):
    """프로젝트의 최근 업데이트 목록 조회"""
    query = '''
    query($id: String!, $first: Int!) {
      project(id: $id) {
        id
        name
        health
        projectUpdates(first: $first) {
          nodes {
            id
            body
            health
            createdAt
            user { name }
          }
        }
      }
    }
    '''
    result = graphql_request(query, {'id': args.project_id, 'first': args.limit})

    if 'errors' in result:
        print(f"Error: {result['errors']}", file=sys.stderr)
        sys.exit(1)

    project = result['data']['project']
    if not project:
        print(f"Error: Project not found: {args.project_id}", file=sys.stderr)
        sys.exit(1)

    output = {
        'project': {
            'id': project['id'],
            'name': project['name'],
            'health': project['health']
        },
        'updates': project['projectUpdates']['nodes']
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

def cmd_create_initiative_update(args):
    """이니셔티브 업데이트 생성"""
    body = Path(args.body_file).read_text(encoding='utf-8')

    query = '''
    mutation($input: InitiativeUpdateCreateInput!) {
      initiativeUpdateCreate(input: $input) {
        success
        initiativeUpdate {
          id
          url
        }
      }
    }
    '''
    variables = {
        'input': {
            'initiativeId': args.initiative_id,
            'body': body,
            'health': args.health
        }
    }

    result = graphql_request(query, variables)

    if 'errors' in result:
        print(f"❌ API 에러: {json.dumps(result['errors'], ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    if result.get('data', {}).get('initiativeUpdateCreate', {}).get('success'):
        update = result['data']['initiativeUpdateCreate']['initiativeUpdate']
        print(f"✅ 이니셔티브 업데이트 생성 완료!")
        print(f"URL: {update['url']}")
    else:
        print(f"❌ 업데이트 생성 실패: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Linear API 헬퍼 - Initiative Update')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # whoami
    subparsers.add_parser('whoami', help='현재 사용자 정보')

    # my-initiatives
    subparsers.add_parser('my-initiatives', help='내가 owner인 이니셔티브 목록')

    # initiative-projects
    p = subparsers.add_parser('initiative-projects', help='이니셔티브의 프로젝트 목록')
    p.add_argument('initiative_id', help='이니셔티브 ID')

    # project-updates
    p = subparsers.add_parser('project-updates', help='프로젝트의 최근 업데이트')
    p.add_argument('project_id', help='프로젝트 ID')
    p.add_argument('--limit', type=int, default=5, help='조회할 업데이트 수 (기본: 5)')

    # create-initiative-update
    p = subparsers.add_parser('create-initiative-update', help='이니셔티브 업데이트 생성')
    p.add_argument('initiative_id', help='이니셔티브 ID')
    p.add_argument('body_file', help='업데이트 내용 마크다운 파일')
    p.add_argument('--health', choices=['onTrack', 'atRisk', 'offTrack'],
                   default='onTrack', help='이니셔티브 상태')

    args = parser.parse_args()

    commands = {
        'whoami': cmd_whoami,
        'my-initiatives': cmd_my_initiatives,
        'initiative-projects': cmd_initiative_projects,
        'project-updates': cmd_project_updates,
        'create-initiative-update': cmd_create_initiative_update,
    }

    commands[args.command](args)

if __name__ == '__main__':
    main()

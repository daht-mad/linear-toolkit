#!/usr/bin/env node

/**
 * Linear Document Creator
 * Usage: node create-doc.mjs <file-path> <project-id> [title]
 */

import fs from 'fs';

const [,, filePath, projectId, customTitle] = process.argv;

if (!filePath || !projectId) {
  console.error(JSON.stringify({
    error: 'Missing required arguments',
    usage: 'node create-doc.mjs <file-path> <project-id> [title]'
  }));
  process.exit(1);
}

// Read file content
let content;
try {
  content = fs.readFileSync(filePath, 'utf8');
} catch (err) {
  console.error(JSON.stringify({ error: `Failed to read file: ${err.message}` }));
  process.exit(1);
}

// Extract title from first heading or use custom title or filename
let title = customTitle;
if (!title) {
  const headingMatch = content.match(/^#\s+(.+)$/m);
  if (headingMatch) {
    title = headingMatch[1];
  } else {
    title = filePath.split('/').pop().replace(/\.md$/, '');
  }
}

// Check for API token
if (!process.env.LINEAR_API_TOKEN) {
  console.error(JSON.stringify({ error: 'LINEAR_API_TOKEN environment variable not set' }));
  process.exit(1);
}

// GraphQL mutation
const query = `
  mutation CreateDoc($input: DocumentCreateInput!) {
    documentCreate(input: $input) {
      success
      document {
        id
        title
      }
    }
  }
`;

const variables = {
  input: {
    title,
    content,
    projectId
  }
};

try {
  const response = await fetch('https://api.linear.app/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': process.env.LINEAR_API_TOKEN
    },
    body: JSON.stringify({ query, variables })
  });

  const result = await response.json();

  if (result.errors) {
    console.error(JSON.stringify({ error: result.errors[0].message }));
    process.exit(1);
  }

  console.log(JSON.stringify({
    success: true,
    document: result.data.documentCreate.document
  }));
} catch (err) {
  console.error(JSON.stringify({ error: `API request failed: ${err.message}` }));
  process.exit(1);
}
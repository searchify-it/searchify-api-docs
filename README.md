# Searchify Client Stream API

This guide explains how to use the Searchify Stream API to get AI-generated responses with search results and citations.

Please ensure you have received a email containing the following items prior to this guide:
- Base URL for the API
- You client portal logins to manage your API Keys

## Overview

The Stream API provides real-time streaming of AI responses based on your configured search data. Each response chunk includes the complete text so far and any search results referenced in that text.

## Authentication

**Use only the Authorization header method for security:**

```bash
Authorization: Bearer your_api_key_here
```

⚠️ **Security Note**: Do not use query parameters or request body for API keys in production.

## Endpoint

```
POST /v1/stream
```

## Request Format

```json
{
  "instance_hash": "your_instance_hash_here",
  "query": "Your question here"
}
```

## Response Format

The API returns Server-Sent Events (SSE) with JSON data in each chunk:

```json
{
  "isDone": false,
  "updatedText": "Complete response text so far...",
  "search_results": [
    {
      "id": "0",
      "snippet": {
        "pre": "Text before the relevant part ",
        "text": "the relevant text snippet",
        "post": " text after the relevant part"
      },
      "source": "example.com",
      "url": "https://example.com/page",
      "title": "Page Title",
      "metadata": {
        "additional": "metadata fields"
      }
    }
  ]
}
```

## Key Features

### 1. Complete Text in Every Chunk
- `updatedText` contains the **entire response text** at each chunk
- You don't need to concatenate chunks - just use the latest `updatedText`
- The text grows incrementally as the AI generates more content

### 2. Citation Extraction
Citations appear as numbered references in the text: `[0]`, `[1]`, `[2]`, etc.

**To extract citations:**
1. Parse the `updatedText` for citation markers like `[0]`, `[1]`
2. Match the numbers to the `id` field in `search_results`
3. Use the corresponding search result for the citation

### 3. Search Results
- Only search results referenced in the current text chunk are included
- Each result contains the full snippet, source, URL, and metadata
- Results are filtered to only show those actually cited

## Simple Example

### JavaScript/Node.js

```javascript
async function streamSearchifyResponse(apiKey, instanceHash, query) {
  const response = await fetch('http://localhost:8000/v1/stream', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      instance_hash: instanceHash,
      query: query
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let fullText = '';
  let citations = new Map();

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6));
          
          // Get the complete text (no need to concatenate)
          fullText = data.updatedText;
          
          // Store search results for citations
          if (data.search_results) {
            data.search_results.forEach(result => {
              citations.set(result.id, result);
            });
          }
          
          // Check if streaming is complete
          if (data.isDone) {
            console.log('Final response:', fullText);
            console.log('Available citations:', citations);
            return { text: fullText, citations };
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

// Usage
const result = await streamSearchifyResponse(
  'your_api_key_here',
  'your_instance_hash_here',
  'What classes do I need for a computer science degree?'
);

// Extract citations from the text
const citationRegex = /\[(\d+)\]/g;
let match;
while ((match = citationRegex.exec(result.text)) !== null) {
  const citationId = match[1];
  const citation = result.citations.get(citationId);
  if (citation) {
    console.log(`Citation [${citationId}]:`, citation.title, citation.url);
  }
}
```

### Python

```python
import requests
import json
import re

def stream_searchify_response(api_key, instance_hash, query):
    url = "http://localhost:8000/v1/stream"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "instance_hash": instance_hash,
        "query": query
    }
    
    response = requests.post(url, json=payload, headers=headers, stream=True)
    response.raise_for_status()
    
    full_text = ""
    citations = {}
    
    for line in response.iter_lines():
        if line and line.startswith(b'data: '):
            data = json.loads(line[6:])  # Remove 'data: ' prefix
            
            # Get complete text (no concatenation needed)
            full_text = data.get('updatedText', '')
            
            # Store search results for citations
            if data.get('search_results'):
                for result in data['search_results']:
                    citations[result['id']] = result
            
            # Check if streaming is complete
            if data.get('isDone'):
                print(f"Final response: {full_text}")
                print(f"Available citations: {citations}")
                return {"text": full_text, "citations": citations}

# Usage
result = stream_searchify_response(
    "your_api_key_here",
    "your_instance_hash_here", 
    "What classes do I need for a computer science degree?"
)

# Extract citations from the text
citation_matches = re.findall(r'\[(\d+)\]', result["text"])
for citation_id in citation_matches:
    if citation_id in result["citations"]:
        citation = result["citations"][citation_id]
        print(f"Citation [{citation_id}]: {citation['title']} - {citation['url']}")
```

### cURL

```bash
curl -X POST "http://localhost:8000/v1/stream" \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "instance_hash": "your_instance_hash_here",
    "query": "What classes do I need for a computer science degree?"
  }' \
  --no-buffer
```

## Important Notes

1. **Complete Text**: Always use `updatedText` - it contains the full response, not just the new part
2. **Citations**: Look for `[0]`, `[1]`, etc. in the text and match to search result IDs
3. **Search Results**: Only results actually cited in the current text chunk are included
4. **Streaming**: The response streams in real-time - you can display text as it arrives
5. **Completion**: Check `isDone: true` to know when the response is complete

## Error Handling

- **401**: Invalid or missing API key
- **403**: API key doesn't have access to the instance
- **404**: Instance not found
- **429**: Rate limit exceeded
- **500**: Internal server error

## Rate Limits

API keys may have usage limits based on your plan. Check the response headers for rate limit information.

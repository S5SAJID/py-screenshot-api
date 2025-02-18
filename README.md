# Website Screenshot API

A serverless API built with FastAPI for capturing website screenshots. This API is designed to work with Vercel's serverless environment and includes API key authentication for security.

## Features

- 🔒 Secure API key authentication
- 📱 Configurable viewport size
- 📜 Full-page screenshot support
- 🚀 Vercel serverless compatible
- ✨ Type-safe implementation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

3. Create a `.env` file with your API key:
```bash
API_KEY=your-secret-api-key-here
```

## Local Development

Run the development server:
```bash
uvicorn api.screenshot:app --reload
```

## API Usage

### Take Screenshot

```bash
curl -X POST https://your-domain.vercel.app/api/screenshot \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "width": 1920,
    "height": 1080,
    "full_page": false
  }'
```

### Request Parameters

- `url` (required): Website URL to screenshot
- `width` (optional): Viewport width (default: 1920)
- `height` (optional): Viewport height (default: 1080)
- `full_page` (optional): Capture full scrollable page (default: false)

## Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy to Vercel:
```bash
vercel
```

Remember to set your API_KEY environment variable in your Vercel project settings.

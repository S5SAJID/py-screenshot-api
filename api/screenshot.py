from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import Response
from pydantic import BaseModel, HttpUrl
from typing import Optional
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Screenshot API",
             description="API for capturing website screenshots",
             version="1.0.0")

# API key security setup
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable not set")

async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """
    Validate API key from request header
    
    Args:
        api_key_header (str): API key from request header
        
    Returns:
        str: Validated API key
        
    Raises:
        HTTPException: If API key is invalid
    """
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=403,
        detail="Invalid API key"
    )

class ScreenshotRequest(BaseModel):
    """Request model for screenshot endpoint"""
    url: HttpUrl
    width: Optional[int] = 1920
    height: Optional[int] = 1080
    full_page: Optional[bool] = False

@app.post("/api/screenshot")
async def take_screenshot(
    request: ScreenshotRequest,
    api_key: str = Depends(get_api_key)
) -> Response:
    """
    Take a screenshot of the specified URL
    
    Args:
        request (ScreenshotRequest): Screenshot request parameters
        api_key (str): Validated API key
        
    Returns:
        Response: Screenshot image in PNG format
        
    Raises:
        HTTPException: If screenshot capture fails
    """
    try:
        async with async_playwright() as p:
            # Launch browser in headless mode
            browser = await p.chromium.launch(headless=True)
            
            # Create new page with specified viewport
            page = await browser.new_page(
                viewport={'width': request.width, 'height': request.height}
            )
            
            # Navigate to URL
            await page.goto(str(request.url), wait_until='networkidle')
            
            # Take screenshot
            screenshot = await page.screenshot(
                full_page=request.full_page,
                type='png'
            )
            
            # Close browser
            await browser.close()
            
            # Return screenshot as response
            return Response(
                content=screenshot,
                media_type="image/png"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to capture screenshot: {str(e)}"
        )

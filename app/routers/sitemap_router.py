from fastapi import APIRouter, Response
from app.data.suburb import suburbs

router = APIRouter()

# Example services
services = ["computer-repair", "laptop-repair", "wifi-repair"]
# Example static pages
static_pages = ["about", "contact", "services"]
# Add other categories or routes you want to include in the sitemap
blog_posts = ["post1", "post2", "post4"]  # Replace with actual blog post slugs if applicable
categories = ["computers", "laptops", "wifi"]

@router.get("/sitemap.xml", response_class=Response)
async def sitemap():
    base_url = "https://infinitech.co.nz"

    # Generate XML sitemap
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # Add homepage URL
    xml += f"  <url>\n"
    xml += f"    <loc>{base_url}/</loc>\n"
    xml += f"    <priority>1.0</priority>\n"
    xml += f"  </url>\n"

    # Add static pages
    for page in static_pages:
        url = f"{base_url}/{page}"
        xml += f"  <url>\n"
        xml += f"    <loc>{url}</loc>\n"
        xml += f"    <priority>0.6</priority>\n"
        xml += f"  </url>\n"
    
    # Add service pages for each suburb
    for suburb in suburbs:
        for service in services:
            url = f"{base_url}/{service}/{suburb}"
            xml += f"  <url>\n"
            xml += f"    <loc>{url}</loc>\n"
            xml += f"    <priority>0.8</priority>\n"
            xml += f"  </url>\n"
    
    # Add category pages
    for category in categories:
        url = f"{base_url}/{category}"
        xml += f"  <url>\n"
        xml += f"    <loc>{url}</loc>\n"
        xml += f"    <priority>0.7</priority>\n"
        xml += f"  </url>\n"
    
    # Add blog posts
    for post in blog_posts:
        url = f"{base_url}/blog/{post}"
        xml += f"  <url>\n"
        xml += f"    <loc>{url}</loc>\n"
        xml += f"    <priority>0.5</priority>\n"
        xml += f"  </url>\n"

    # Add 404 error page
    xml += f"  <url>\n"
    xml += f"    <loc>{base_url}/404</loc>\n"
    xml += f"    <priority>0.3</priority>\n"
    xml += f"  </url>\n"
    
    # Close the URL set
    xml += "</urlset>"

    return Response(content=xml, media_type="application/xml")

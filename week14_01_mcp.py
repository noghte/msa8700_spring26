from fastmcp import FastMCP
import pandas as pd

DF = pd.read_csv("amazon_reviews.csv")

mcp = FastMCP("Demo 🚀")

@mcp.tool
def get_brand_stats(brand_name: str) -> dict:
    """Return average rating and review count for a brand."""
    mask = DF["reviewText"].str.lower().str.contains(brand_name.lower())
    subset = DF[mask]
    if subset.empty:
        return {"error": f"No reviews found for {brand_name}"}
    return {
        "brand": brand_name.capitalize(),
        "review_count": len(subset),
        "avg_rating": round(float(subset["overall"].astype(float).mean()),2)
    }

if __name__ == "__main__":
     mcp.run(transport="http", host="0.0.0.0", port=8000)
     # http://10.250.77.111:8000/mcp
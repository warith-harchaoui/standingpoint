# AWS

## Interpretation

The positioning map uses a two-dimensional grid to compare cloud service providers based on their performance across four key dimensions: Ease of Use (left), Scalability (right), Affordability (bottom), and Flexibility (top). At the top-right corner is AWS, which leads in both Scalability and Flexibility. This indicates that AWS excels at handling large-scale operations efficiently while also offering a high degree of flexibility for various use cases.

The reference point, AWS, stands out as the best performer overall due to its strong presence across all dimensions. Microsoft Azure is another notable leader, achieving top rankings in both Scalability and Flexibility but slightly trailing AWS on Affordability. IBM Cloud excels particularly in Scalability, suggesting it's a robust choice for businesses needing scalable infrastructure.

The leaderboard reflects these performances with AWS leading the pack, followed by Microsoft Azure, Google Cloud, IBM Cloud, Alibaba Cloud, Cloudflare, Oracle Cloud, and Vercel. This ranking is determined by combining scores across all four dimensions, highlighting AWS as the clear leader in cloud services.

## Axes

- **Horizontal — Ease of Use ↔ Scalability** (55% of variance). Columns by weight: Compute Breadth (+0.54) · Enterprise Trust (+0.44) · Managed AI/ML (+0.35) · Global Reach (+0.05) · Pricing Value (-0.15) · Serverless (-0.20) · Developer Experience (-0.57).
- **Vertical — Affordability ↔ Flexibility** (28% of variance). Columns by weight: Serverless (+0.59) · Global Reach (+0.52) · Developer Experience (+0.30) · Managed AI/ML (+0.26) · Enterprise Trust (+0.22) · Compute Breadth (+0.03) · Pricing Value (-0.41).
- Together the two axes retain **84%** of the total variation; the reference was rotated +51.1° to reach the top-right.

## Highlighted approaches

- **Leader (reference):** AWS
- **Weakest overall:** DigitalOcean (lowest projection on the leader diagonal)
- **Strongest toward Flexibility:** Microsoft Azure (challenger furthest up the vertical axis)
- **Strongest toward Scalability:** IBM Cloud (challenger furthest along the horizontal axis)

## Leaderboard (by combined axis score)

1. AWS  (+2.20, +2.55)
2. Microsoft Azure  (+2.20, +2.55)
3. Google Cloud  (+1.38, +1.84)
4. IBM Cloud  (+1.77, +0.04)
5. Alibaba Cloud  (+1.08, +0.50)
6. Cloudflare  (-1.20, +2.32)
7. Oracle Cloud  (+1.26, -0.76)
8. Vercel  (-2.20, +1.96)
9. Fly.io  (-1.24, +0.73)
10. Render  (-1.82, +0.53)
11. Vast.ai  (-0.13, -2.24)
12. Hetzner  (-0.89, -2.55)
13. DigitalOcean  (-2.09, -1.57)

*Coordinates are PCA units; see the companion YAML for full coefficients.*

# AWS

## Interpretation

The positioning map uses a two-dimensional grid to compare cloud service providers based on ease of use, scalability, affordability, and flexibility. The horizontal axis represents these dimensions, with "Ease of Use" on the left and "Scalability" on the right. Similarly, the vertical axis measures from "Affordability" at the bottom to "Flexibility" at the top.

Amazon Web Services (AWS) leads in scalability and affordability but lags slightly behind Microsoft Azure when it comes to flexibility. Microsoft Azure excels particularly in its ability to offer a wide range of services, making it highly flexible despite not being as affordable or scalable as AWS. IBM Cloud stands out for its strong performance in scalability, which is reflected by its position furthest towards the right on the map.

The leaderboard reveals that AWS maintains the top spot with a combined score reflecting its overall dominance across all dimensions. Microsoft Azure and Google Cloud follow closely behind, showcasing robust capabilities in both flexibility and scalability. IBM Cloud's standout feature of scalability makes it a notable challenger for cloud service providers aiming to handle large-scale applications efficiently. Alibaba Cloud, Cloudflare, Oracle Cloud, and Vercel also occupy significant positions on the map, each contributing unique strengths that cater to specific needs within their respective niches.

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

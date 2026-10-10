# Hookagé

Handmade crochet wear for women, men, kids, and the beach, plus custom crochet designs made to order. This repository contains the Hookagé storefront: a fast, static website built with plain HTML, CSS, and JavaScript.

**Live site:** [https://yourdomain.com](https://yourdomain.com)

---

## Features

- **Shop by category:** Women, Men, Beachwear, Kids, Bags, Hats, and Socks & Slippers, each with its own page
- **Product pages:** size selection, add to cart, wishlist, and related pieces
- **Search:** live suggestions in the header, plus a search box on every shop page
- **Wishlist:** save pieces with a heart, view them on a dedicated page, and add them to the cart (kept between visits)
- **Cart and checkout:** a cart that persists across pages, delivery fees by region, and checkout via WhatsApp with a ready-written order message
- **Custom orders:** a four-step request form with a live price estimate, sent through WhatsApp
- **Crochet Academy, Community, About, Contact, and FAQ** pages
- **Light and dark mode**, switchable from the header or footer
- **Animated logo and opening screen**, which respect the "reduce motion" setting
- **SEO ready:** unique titles and descriptions, canonical links, Open Graph and Twitter cards, structured data (JSON-LD), sitemap, and robots file
- **Responsive and accessible:** mobile-first layout, keyboard navigation, skip link, and labeled controls

## Tech stack

- HTML5, CSS3, and vanilla JavaScript (no framework, no build step to run the site)
- A small Python script (`tools/build.py`) that generates the static pages from the product data
- Hosted on [Vercel](https://vercel.com)

## Project structure

```
.
├── index.html, shop.html, ...    Generated pages (one per category, product, and topic)
├── styles.css                    All styling, including light and dark themes
├── script.js                     Cart, wishlist, search, custom order form, theme, and sliders
├── config.js                     Site settings (WhatsApp number, delivery fees, photo overrides)
├── products.js                   Product data for the browser (generated)
├── sitemap.xml, robots.txt       Search engine files (generated)
├── site.webmanifest, 404.html
├── assets/
│   ├── images/                   Product, category, and banner photos
│   └── favicon and app icons
└── tools/
    ├── build.py                  Page generator
    ├── data.py                   Products, categories, and social links
    └── templates/                Page text for About, FAQ, Custom Order, and more
```

## Getting started

Clone the repository and open it locally:

```bash
git clone https://github.com/[your-username]/[your-repo].git
cd [your-repo]
```

Open `index.html` in a browser, or serve the folder locally for a more accurate preview:

```bash
python3 -m http.server 8000
```

Then visit <http://localhost:8000>.

## Configuration

Site settings live in `config.js`:

| Setting                     | What it does                                                 |
| --------------------------- | ------------------------------------------------------------ |
| `WA`                        | WhatsApp number for orders (country code first, digits only) |
| `FREE`                      | Order total that qualifies for free delivery (Nigeria)       |
| `REG`                       | Delivery fees by region                                      |
| `PHOTOS`                    | Optional photo overrides, keyed by product name              |
| `HERO_VIDEO`, `HERO_POSTER` | Optional hero video and poster image                         |

Social media links are set in `tools/data.py` under `SOCIAL`.

## Managing products

Products and categories are defined in `tools/data.py`. Each product is one line with its address name, display name, category, price, image name, badge, rating, review count, short type, description, and search keywords.

To add or change a product:

1. Add the product photo to `assets/images/` using the image name from the product line.
2. Edit or add the product line in `tools/data.py`.
3. Regenerate the pages:

```bash
pip install pillow
python3 tools/build.py --url https://yourdomain.com
```

The script rebuilds every page, `products.js`, the sitemap, and the robots file.

## Images

- **Product photos:** portrait 4:5, about 800 x 1000 px, saved as `.jpg`
- **Home banner (`hero.jpg`):** wide, about 1600 x 900 px
- **Category tiles (`cat-*.jpg`):** landscape 3:2, about 900 x 600 px
- Keep each file under about 150 KB so pages load quickly

To replace a photo, save the new file over the old one with the same name, or point to a different file in the `PHOTOS` setting in `config.js`.

## SEO

Every page has its own title, meta description, and canonical link. Product pages include `Product` structured data, category pages include `CollectionPage` data, and the FAQ page includes `FAQPage` data. After deploying:

1. Set your real domain with the build command above.
2. Submit `https://yourdomain.com/sitemap.xml` to Google Search Console.
3. Add ratings to the structured data only once you have real customer reviews.

## Deployment

The site is plain static files, so it can be hosted anywhere. To deploy on Vercel:

1. Push this repository to GitHub.
2. In Vercel, choose **Add New → Project** and import the repository.
3. Leave the framework preset as **Other** and select **Deploy**.
4. Add your custom domain under **Settings → Domains**.

Every push to the main branch redeploys the site automatically.

## Browser support

Current versions of Chrome, Edge, Firefox, and Safari, on desktop and mobile.

## Roadmap

- [ ] Online payments with Paystack
- [ ] Order tracking connected to real orders
- [ ] Newsletter signup connected to an email service
- [ ] Customer reviews

## License

All rights reserved © [Year] Hookagé. Product photos and brand assets may not be reused without permission.

## Contact

Questions, orders, or custom requests: [hello@yourdomain.com](mailto:hello@yourdomain.com) or message us on WhatsApp.

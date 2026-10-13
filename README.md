# Hookagé website

Plain HTML, CSS, and JavaScript. Every page is a real file with its own address, so search engines can find and rank each one. No installs needed to view it.

## Open it
Open `index.html` in a browser. To test like a live site: `python3 -m http.server` in this folder, then visit http://localhost:8000.

## Pages (57)
Home, Shop (all), 7 category pages (Women, Men, Beachwear, Kids, Bags, Hats, Socks & Slippers), 38 product pages, Custom crochet, Learn, Community, About, Contact, FAQ, Cart, Track order, Wishlist, and a 404 page.

## Search
- **Header search:** tap the magnifier on any page. As you type, it shows matching pieces with photos and prices. Press Enter or choose "See all results" for a full results page.
- **On-page search:** the Shop page and every category page have a search box that filters instantly.
- It looks at the name, category, description, and hidden keywords for each product (so "bikini", "mesh", "checker", or "granny" all work). Add or edit keywords in the last field of each product in `tools/data.py`.

## Add or change products
Everything is in `tools/data.py`. Each product is one line: web address name, display name, category, price, image name, badge, rating, review count, short type (used for page titles), description, and search keywords. Add the photo to `assets/images/` using the image name, then run `python3 tools/build.py`. Categories, their sizes, and their tile photos are in the `CATEGORIES` block of the same file.

## Your photos
Replace any photo by saving a new JPG over the file with the same name in `assets/images/`. Product photos are named after the product (for example `striped-bodycon-dress.jpg`) and look best at 4:5 portrait, about 800 x 1000 px. The home banner is `hero.jpg` (wide, 1600 x 900), category tiles are `cat-*.jpg` (landscape 3:2), and `custom.jpg`, `com-1` to `com-5`, and `ac-1` to `ac-4` fill the other sections. To use a different file name, add it to `PHOTOS` in `config.js`.

## Logo animation and opening intro
- **Hover:** the hook wiggles and the yarn redraws, then right after, the letters of "Hookagé" ripple in a wave.
- **Opening intro:** when the site is first opened (and every time it is reloaded) a green screen plays the same logo animation with the wavy name, then lifts away to reveal the site. It waits for the page to finish loading, so slow connections see the animation instead of a blank page. It does not replay when you move between pages, and it is skipped for visitors who have reduced motion turned on.
- Speed and timing are in `styles.css` (search for "wavy brand name") and `script.js` (search for "opening intro").

## Social links
The footer shows WhatsApp, TikTok, Instagram, and Pinterest icons. The links are placeholders. Set your real accounts in `SOCIAL` inside `tools/data.py`, then run `python3 tools/build.py`.

## Wishlist
Tap the heart on any piece to save it. Saved pieces are counted on the heart in the header, kept on the device between visits, listed on `wishlist.html`, and can be removed, added to the cart one by one, or all at once.

## Before you launch: SEO checklist
1. **Set your real domain.** The files use the placeholder `https://www.hookage.store`. Run `python3 tools/build.py --url https://yourdomain.com` (needs Python and Pillow: `pip install pillow`). This rewrites every page's canonical link, social tags, sitemap, and robots file.
2. **Submit the sitemap.** Create a free Google Search Console account, verify your domain, and submit `https://yourdomain.com/sitemap.xml`. Do the same in Bing Webmaster Tools.
3. **Upload your own photos** (see Your photos above). The image descriptions for search engines and screen readers are generated from each product's name, so give every product a clear name in `tools/data.py`.
4. **Write unique product text.** Edit the descriptions in `tools/data.py`, then rebuild. Each product page should read differently from the others.
5. **Add real reviews before adding ratings.** The star ratings on the pages are sample data, so they are deliberately left out of the structured data. Marking up ratings that are not real reviews breaks Google's rules.
6. **Create a Google Business Profile** if you serve customers locally, and link your social accounts to the site.
7. **Test speed and sharing.** Check the live site at https://pagespeed.web.dev, and paste a page link into WhatsApp or Facebook's Sharing Debugger to see the share image.

## What is already built in
- Unique title and description on every page, a canonical link, and a single main heading per page
- Social sharing tags (Open Graph and Twitter) with a share image at `assets/images/og-image.jpg`
- Structured data (JSON-LD): online store and site search on the home page, Product and Breadcrumb on product pages, Collection lists on category pages, and FAQ on the FAQ page
- `sitemap.xml` and `robots.txt` (cart, tracking, and wishlist pages are kept out of search)
- Product and category content is in the page's HTML itself, not drawn by JavaScript, so crawlers see it
- Image width and height set, lazy loading, a preloaded hero image, and fast-loading fonts
- Favicon, app icons, and a web manifest; skip-to-content link and accessible labels

## Change content
- **Products, prices, categories:** `tools/data.py`, then run the build command above.
- **Page text** (about, FAQ, custom form, home sections): `tools/templates/`, then rebuild.
- **WhatsApp number, delivery fees, hero video:** `config.js`.
- **Colours and spacing:** `styles.css`.
Replace `hello@hookage.store` and `2340000000000` in `tools/data.py`, `tools/templates/contact.html`, and `config.js`.

## Checkout via WhatsApp
On the cart page, "Checkout via WhatsApp" sits beside "Pay with Paystack". It checks the name, phone, and address, then opens WhatsApp with a ready-written order: each item with size, quantity, price, and a link to the product, plus subtotal, delivery, total, and the customer's details. The message also appears on the page with a Copy button in case WhatsApp does not open. The cart is kept, so nothing is lost if the customer comes back. Your number is `WA` in `config.js`.

## Still a prototype
The cart works across pages but checkout is a placeholder (connect Paystack), order tracking recognises only `HK-1042`, and email signup does not save addresses. For real orders and stock, use Shopify or WooCommerce or add a backend.

## Deploy for free
Upload this whole folder to Netlify (drag and drop), Vercel, GitHub Pages, or Cloudflare Pages, and point your domain at it. Make sure your host serves `404.html` for missing pages.

const PRODUCTS = [
  {
    title: 'Fresh Farm Milk',
    image: '/images/products/milk.jpg', // TODO: add this image to public/images/products/
    description: 'Fresh, quality milk supplied daily. Available for bulk and retail orders.',
    tag: 'Daily supply',
  },
  {
    title: 'Dairy Cattle',
    image: '/images/animals/cows.jpg',
    description: 'Healthy, vaccinated Friesian and Ayrshire cattle, raised on our own farm.',
    tag: 'By inquiry',
  },
  {
    title: 'Goats & Sheep',
    image: '/images/animals/goats.jpg',
    description: 'Alpine goats and Dorper sheep, well-fed and health-checked, ready for sale.',
    tag: 'By inquiry',
  },
];

function Products() {
  return (
    <section id="products" className="section section-alt">
      <div className="section-header">
        <span className="section-eyebrow">Straight from our farm</span>
        <h2>Milk &amp; Cattle for Sale</h2>
        <p>Interested in buying? Reach out below and we'll get back to you directly.</p>
      </div>

      <div className="product-grid">
        {PRODUCTS.map((p) => (
          <div className="product-card" key={p.title}>
            <div
              className="product-card-image"
              style={{ backgroundImage: `url(${p.image})` }}
            />
            <div className="product-card-body">
              <span className="pill pill-success">{p.tag}</span>
              <h3>{p.title}</h3>
              <p>{p.description}</p>
              <a href="#contact" className="card-link">
                Enquire now →
              </a>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Products;
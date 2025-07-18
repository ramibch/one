function createpdf(title, company_name, company_address, to_heading, to, ship_to_heading, ship_to, number_heading, number, date_heading, date, order_number_heading, order_number, article_title_text, article_quantity_text, article_price_text, article_total_text, terms_heading, terms, subtotal, subtotal_heading, subtotal_str, vat, vat_heading, discount, discount_heading, subtotal_with_discount, subtotal_with_discount_str, subtotal_with_discount_heading, total, total_heading, total_str, products, settings_shipto_active, settings_discount_active) {
  const doc = jsPDF("p", "mm", [297, 210]);
  doc.setFontSize(10);
  const titleWidth = doc.getTextWidth(title);

  doc.text(title, 20, 20);
  doc.line(20, 21, 20 + titleWidth, 21)
  doc.text(company_name, 20, 30);
  doc.text(company_address, 20, 40);

  doc.text(`${number_heading}: ${number}`, 120, 30);
  doc.text(`${date_heading}: ${date}`, 120, 40);
  doc.text(`${order_number_heading}: ${order_number}`, 120, 50);


  doc.text(to_heading, 20, 80);
  doc.text(to, 20, 90);
  if(settings_shipto_active){
    doc.text(ship_to_heading, 100, 80);
    doc.text(ship_to, 100, 90);
  }

  doc.text(article_title_text, 20, 120);
  doc.text(article_quantity_text, 120, 120);
  doc.text(article_price_text, 140, 120);
  doc.text(article_total_text, 160, 120);
  products.forEach((item, index) => {
    let h_product = parseInt(130 + index*8);
    doc.text(item[0], 20, h_product);
    doc.text(String(item[1]), 120, h_product);
    doc.text(String(item[2]), 140, h_product);
    doc.text(String(item[3]), 160, h_product);
  });

  const totalText = `${total_heading}: ${total_str}`
  const totalTextWidth = doc.getTextWidth(totalText)*1.05;

  doc.text(`${subtotal_heading}: ${subtotal_with_discount_str} `, 120, 220);

  if(settings_discount_active){
    doc.text(`${discount_heading}: ${discount}`, 120, 230);
    doc.text(`${subtotal_with_discount_heading}: ${subtotal_with_discount_str}`, 120, 240);
    doc.text(`${vat_heading}: ${vat}`, 120, 250);
    doc.text(totalText, 120, 260);
    doc.line(120, 261, 120 + totalTextWidth, 261)
  }else{
    doc.text(`${vat_heading}: ${vat}`, 120, 230);
    doc.text(totalText, 120, 240);
    doc.line(120, 241, 120 + totalTextWidth, 241)
  }

  doc.text(terms_heading, 20, 260);
  var splitTerms = doc.splitTextToSize(terms, 175);
  doc.text(splitTerms, 20, 270);

  doc.save(`${title}_${number}.pdf`);
}

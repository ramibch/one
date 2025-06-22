// sortable elements
document.addEventListener('htmx:load', function () {
  const sortableEl = document.querySelector('.sortable');
  if (sortableEl) {
    new Sortable(sortableEl, {
      handle: '.handle',
      animation: 150,
      ghostClass: 'blue-background-class',
      // onEnd: function () {
      //   const ids = Array.from(sortableEl.children)
      //     .map(el => el.dataset.id)
      //     .filter(Boolean); // removes empty, null, or undefined

      //   document.getElementById('order-input').value = ids.join(',');
      //   htmx.trigger(sortableEl, 'end');  // HTMX will include `order` in the POST
      // }
      onEnd: function () {
        const sortableItems = Array.from(sortableEl.children);
        sortableItems.forEach((el, index) => {
          const input = el.querySelector('input[name="order"]');
          if (input) {
            el.parentNode.appendChild(el); // move element in DOM
          }
        });

        htmx.trigger(sortableEl, 'end');
      }
    });
  }
});

// check if the image element is in the DOM
function pollImageToCrop(data) {
  console.log(data);
  const element = document.getElementById("image-to-crop");

  if (element) {
    // Once the image element showed in the DOM, we can start the cropper event
    startCropperEvent(element);
  } else {
    setTimeout(pollImageToCrop, 200); // try again in 200 milliseconds
  }
  delete element;
}


function startCropperEvent(element) {

  const cropper = new Cropper(element, {
    viewMode: 3,
    aspectRatio: 1 / 1,
    responsive: true,
    guides: true,
    zoomable: false,
    autoCropArea: 0.9,
    movable: false,
    scalable: true,
    data: getInitData(),
    crop(event) {
      setImageCropProperties(event.detail.x, event.detail.y, event.detail.width, event.detail.height);
    },
  });
}


// this function sets the cropping properties from the cropperjs library to the form inputs
function setImageCropProperties(x, y, width, height) {
  document.getElementById("id_crop_x").setAttribute("value", Math.round(x));
  document.getElementById("id_crop_y").setAttribute("value", Math.round(y));
  document.getElementById("id_crop_width").setAttribute("value", Math.round(width));
  document.getElementById("id_crop_height").setAttribute("value", Math.round(height));
}


function getInitData() {

  const data = {
    x: parseInt(document.getElementById("id_crop_x").value),
    y: parseInt(document.getElementById("id_crop_y").value),
    width: parseInt(document.getElementById("id_crop_width").value),
    height: parseInt(document.getElementById("id_crop_height").value),
  };
  console.log(data);
  return data;

}

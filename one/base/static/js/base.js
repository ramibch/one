document.addEventListener('htmx:load', function () {
  const sortableEls = document.querySelectorAll('.sortable');

  sortableEls.forEach((sortableEl) => {
    new Sortable(sortableEl, {
      handle: '.handle',
      animation: 150,
      onEnd: function () {
        const sortableItems = Array.from(sortableEl.children);
        sortableItems.forEach((el) => {
          const input = el.querySelector('input[name="order"]');
          if (input) {
            sortableEl.appendChild(el); // ensure proper DOM order
          }
        });
        htmx.trigger(sortableEl, 'end');
      }
    });
  });
});


// check if the image element is in the DOM
function pollImageToCrop(data) {
  console.log(data);
  const element = document.getElementById("image-to-crop");

  if (element) {
    // Once the image element showed in the DOM, we can start the cropper event
    startCropper(element);
  } else {
    setTimeout(pollImageToCrop, 200); // try again in 200 milliseconds
  }
  delete element;
}


function startCropper(element) {

  const cropper = new Cropper(element, {
    viewMode: 3,
    aspectRatio: 1 / 1,
    responsive: true,
    guides: true,
    zoomable: false,
    autoCropArea: 0.9,
    movable: false,
    scalable: true,
    data: getCropInitData(),
    crop(event) {
      setImageCropProperties(
        event.detail.x,
        event.detail.y,
        event.detail.width,
        event.detail.height,
      );
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


function getCropInitData() {
  const data = {
    x: parseInt(document.getElementById("id_crop_x").value),
    y: parseInt(document.getElementById("id_crop_y").value),
    width: parseInt(document.getElementById("id_crop_width").value),
    height: parseInt(document.getElementById("id_crop_height").value),
  };
  console.log(data);
  return data;
}

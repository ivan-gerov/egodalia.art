import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";

import "./main.css";

const LOADING_GIF =
  "https://storage.googleapis.com/egodalia-art.appspot.com/loading.gif";

function MainImageUploader() {
  const [image, setImage] = useState(
    document
      .getElementById("django_main_image_hidden_input")
      ?.getAttribute("initial_value") || null,
  );
  const [loading, setLoading] = useState(false);

  async function handleImageChange(e) {
    if (e.target.files[0]) {
      let imageFile = e.target.files[0];

      // If larger than 4.5 mbs (Vercel 413: FUNCTION_PAYLOAD_TOO_LARGE)
      if (imageFile.size / 1024 ** 2 >= 4.5) {
        setImage(LOADING_GIF);
        setLoading(true);
        try {
          const resizedImage = await resizeImage({
            file: imageFile,
            maxSize: 1200,
          });
          setImage(resizedImage);
          setLoading(false);
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(resizedImage);
          e.target.files = dataTransfer.files;
        } catch (err) {
          console.log(`Couldn't resize image ${imageFile} ${err}`);
        }
      } else {
        setImage(imageFile);
        setLoading(false);
      }
      document.getElementById("django_main_image_deleted_hidden_input").value =
        "";
    }
  }

  function handleDeleteImage() {
    setImage(null);
    document.getElementById("django_main_image_deleted_hidden_input").value =
      "true";
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <button
        type="button"
        className="upload-images-button"
        onClick={(e) => {
          e.preventDefault();
          const fileInput = document.getElementById(
            "django_main_image_hidden_input",
          );
          if (fileInput) {
            fileInput.onchange = handleImageChange;
            fileInput.click();
          }
        }}
      >
        Main image
      </button>
      {image && (
        <div
          style={{
            position: "relative",
            display: "inline-block",
            width: "fit-content",
          }}
        >
          {!loading && (
            <button
              type="button"
              className="delete-image-button"
              onClick={() => {
                handleDeleteImage();
              }}
            >
              +
            </button>
          )}
          <img
            src={image instanceof File ? URL.createObjectURL(image) : image}
            style={{ width: "300px", height: "300px" }}
          />
        </div>
      )}
    </div>
  );
}

function AdditionalImagesUploader() {
  const [images, setImages] = useState(
    Array.from(
      document
        .getElementById("django_multi_image_hidden_input")
        ?.getAttribute("initial_values")
        ? JSON.parse(
            JSON.parse(
              document
                .getElementById("django_multi_image_hidden_input")
                .getAttribute("initial_values"),
            ),
          )
        : [],
    ),
  );
  const [deletedImages, setDeletedImages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const dataTransfer = new DataTransfer();
    const alreadyUploadedImages = [];
    for (let file of images) {
      if (!(file instanceof File) && file?.url) {
        alreadyUploadedImages.push(file);
      } else {
        dataTransfer.items.add(file);
      }
    }

    const djangoMultiImageHiddentInput = document.getElementById(
      "django_already_uploaded_multi_image_hidden_input",
    );

    if (djangoMultiImageHiddentInput) {
      djangoMultiImageHiddentInput.value = JSON.stringify(
        alreadyUploadedImages,
      );
      document.getElementById("django_multi_image_hidden_input").files =
        dataTransfer.files;
    }
  }, [images, setImages]);

  useEffect(() => {
    document.getElementById(
      "django_additional_images_deleted_hidden_input",
    ).value = JSON.stringify(deletedImages);
  }, [deletedImages, setDeletedImages]);

  const handleImageChange = async (e) => {
    const currentImages = images.map((img) => img.name);
    const imagesToAdd = [];

    setLoading(true);
    for (let file of e.target.files) {
      if (
        !currentImages.includes(file.name) &&
        !imagesToAdd.map((img) => img.name).includes(file.name)
      ) {
        let imageFile = file;
        if (imageFile.size / 1024 ** 2 >= 4.5) {
          try {
            imageFile = await resizeImage({
              file: imageFile,
              maxSize: 1200,
            });
          } catch (err) {
            log(`Couldn't resize image ${imageFile} ${err}`);
          }
        }

        imagesToAdd.push(imageFile);
      }

      if (deletedImages.includes(file.name)) {
        setDeletedImages(deletedImages.filter((img) => img.name != file.name));
      }
    }

    if (imagesToAdd.length > 0) {
      setImages([...images, ...imagesToAdd]);
    }
    setLoading(false);
  };

  const handleDeleteImage = (imageToDeleteName) => {
    setImages(images.filter((image) => image.name !== imageToDeleteName));
    setDeletedImages([...deletedImages, imageToDeleteName]);
  };

  return (
    <div>
      <button
        type="button"
        className="upload-images-button"
        onClick={(e) => {
          e.preventDefault();
          const fileInput = document.getElementById(
            "django_multi_image_hidden_input",
          );
          if (fileInput) {
            fileInput.onchange = handleImageChange; // Attach event listener here
            fileInput.click(); // Open file dialog
          }
        }}
      >
        Additional images
      </button>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          gap: "1rem",
          flexWrap: "wrap",
          marginTop: "1rem",
        }}
      >
        {loading ? (
          <img src={LOADING_GIF} style={{ width: "300px", height: "300px" }} />
        ) : (
          <>
            {images.map((image, index) => (
              <div
                key={index}
                style={{ position: "relative", display: "inline-block" }}
              >
                <button
                  type="button"
                  className="delete-image-button"
                  onClick={() => {
                    handleDeleteImage(image.name);
                  }}
                >
                  +
                </button>
                <img
                  src={image.url || URL.createObjectURL(image)}
                  alt={`image-${index}`}
                  style={{ width: "300px", height: "300px" }}
                />
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("multi_image_manager_root")).render(
  <React.StrictMode>
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <MainImageUploader />
      <hr />
      <AdditionalImagesUploader />
    </div>
  </React.StrictMode>,
);

function resizeImage(settings) {
  let file = settings.file;
  let maxSize = settings.maxSize;
  let reader = new FileReader();
  let image = new Image();
  let canvas = document.createElement("canvas");
  let dataURItoBlob = function (dataURI) {
    let bytes =
      dataURI.split(",")[0].indexOf("base64") >= 0
        ? atob(dataURI.split(",")[1])
        : unescape(dataURI.split(",")[1]);
    let mime = dataURI.split(",")[0].split(":")[1].split(";")[0];
    let max = bytes.length;
    let ia = new Uint8Array(max);
    for (let i = 0; i < max; i++) ia[i] = bytes.charCodeAt(i);
    return new Blob([ia], { type: mime });
  };
  let resize = function () {
    let width = image.width;
    let height = image.height;
    if (width > height) {
      if (width > maxSize) {
        height *= maxSize / width;
        width = maxSize;
      }
    } else {
      if (height > maxSize) {
        width *= maxSize / height;
        height = maxSize;
      }
    }
    canvas.width = width;
    canvas.height = height;
    canvas.getContext("2d").drawImage(image, 0, 0, width, height);
    let dataUrl = canvas.toDataURL("image/jpeg");
    return dataURItoBlob(dataUrl);
  };
  return new Promise((resolve, reject) => {
    if (!file.type.match(/image.*/)) {
      reject(new Error("Not an image"));
      return;
    }
    reader.onload = function (readerEvent) {
      image.onload = function () {
        let resizedBlob = resize();
        let resizedFile = new File([resizedBlob], file.name, {
          type: resizedBlob.type,
          lastModified: Date.now(),
        });
        resolve(resizedFile);
      };
      image.src = readerEvent.target.result;
    };
    reader.readAsDataURL(file);
  });
}

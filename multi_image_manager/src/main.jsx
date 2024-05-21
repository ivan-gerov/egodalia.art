import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";

import "./main.css";

function MainImageUploader() {
  const [image, setImage] = useState(
    document
      .getElementById("django_main_image_hidden_input")
      ?.getAttribute("initial_value") || null
  );

  function handleImageChange(e) {
    if (e.target.files[0]) {
      setImage(e.target.files[0]);
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
            "django_main_image_hidden_input"
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
          <button
            type="button"
            className="delete-image-button"
            onClick={() => {
              handleDeleteImage();
            }}
          >
            +
          </button>
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
                .getAttribute("initial_values")
            )
          )
        : []
    )
  );
  const [deletedImages, setDeletedImages] = useState([]);

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
      "django_already_uploaded_multi_image_hidden_input"
    );

    if (djangoMultiImageHiddentInput) {
      djangoMultiImageHiddentInput.value = JSON.stringify(
        alreadyUploadedImages
      );
      document.getElementById("django_multi_image_hidden_input").files =
        dataTransfer.files;
    }
  }, [images, setImages]);

  useEffect(() => {
    document.getElementById(
      "django_additional_images_deleted_hidden_input"
    ).value = JSON.stringify(deletedImages);
  }, [deletedImages, setDeletedImages]);

  const handleImageChange = (e) => {
    const currentImages = images.map((img) => img.name);
    const imagesToAdd = [];

    for (let file of e.target.files) {
      if (
        !currentImages.includes(file.name) &&
        !imagesToAdd.map((img) => img.name).includes(file.name)
      ) {
        imagesToAdd.push(file);
      }

      if (deletedImages.includes(file.name)) {
        setDeletedImages(deletedImages.filter((img) => img.name != file.name));
      }
    }

    if (imagesToAdd.length > 0) {
      setImages([...images, ...imagesToAdd]);
    }
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
            "django_multi_image_hidden_input"
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
  </React.StrictMode>
);

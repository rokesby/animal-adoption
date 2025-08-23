import { useState, useEffect } from "react";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";

export default function StandardImageList({ files }) {
  
  const [imageBlobs, setImageBlobs] = useState([files]);

  const handleImageFiles = () => {
    if (files) {
        try {
            const imagesWithUrl = [...files].map(file => {
            return {
                ...file,
                url: URL.createObjectURL(file),
            };
            })
            setImageBlobs(imagesWithUrl);
                
        } catch (error) {
            console.log('Error:', error)
            throw new Error("Error", error);
        }
    }
    else {
        console.log('No files')
    }
    
  };

  useEffect(() => {
    try {
      handleImageFiles();
    } catch (error) {
      console.log("error: ", error);
    }
  }, [files]);

  return (
    <>
      {imageBlobs.length > 0 ? (
              <ImageList sx={{ width: 500, height: 450 }} cols={3} rowHeight={164}>
                {imageBlobs.map((image) => (
                    <ImageListItem key={image.name} >
                    <img
                        srcSet={image.url}
                        src={image.url}
                        alt={image.name}
                        loading="lazy"
                        sx={{ objectFit:'contain'}}
                    />
                    </ImageListItem>
                ))}
            </ImageList>
      ) : (
        <div>
          <p> no animals</p>
        </div>
      )}
    </>
  );
}

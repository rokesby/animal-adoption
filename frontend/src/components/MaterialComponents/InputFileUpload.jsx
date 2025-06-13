import * as React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';


const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

// FileList {0: File, length: 1}
// {0: FilelastModified: 1748177229455,
//     lastModifiedDate: Sun May 25 2025 13:47:09 GMT+0100 (British Summer Time) {},
//     name: "cat_image_3.png",
//     size: 303545,
//     type: "image/png",
//     webkitRelativePath: "",
//     [[Prototype]]: Filelength: 1[[Prototype]]: FileList}

// Add function to handle files
// Store files in state?
// validate image format
// validate image size
// Only upload once animal has been created to avoid orphan data
// set limit of 10

// const handleFileUploadData = (e) => {
//     console.log(e.target.files)
//     if(e.target.files) {
//         setFiles(e.target.files)
//     }
// }

export const InputFileUpload = () => {
  return (
    <Button
      component="label"
      role={undefined}
      variant="contained"
    //   tabIndex={-1}
      startIcon={<CloudUploadIcon />}
    >
      Upload files (Max 10)
      <VisuallyHiddenInput
        type="file"
        onChange={(e) => handleFileUploadData(e)}
        multiple
      />
    </Button>
  );
}

export default InputFileUpload;
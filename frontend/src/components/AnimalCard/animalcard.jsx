import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";
import { buildImageUrl } from "../../utils/gcpUtils";
// import { getProfileImage } from "../../services/animals";

const AnimalCard = ({
  id,
  name,
  age,
  breed,
  location,
  button1Text,
  linkUrl,
  shelter_id,
  profileImageId
}) => {
  const [profileImage, setProfileImage] = useState("/profile_placeholder.png");

  // useEffect( () => {
  //   const fetchProfileImage = async () => {
  //     try {
  //       const image = await getProfileImage(id)
  //       if (image) {
  //         setProfileImage(image)
  //       }
  //       else {
  //         setProfileImage("../../public/profile_placeholder.png")
  //       }
  //     } catch (error) {
  //       console.error('error', error)
  //     }
  //   }
  //   fetchProfileImage()
  // }, [])
  useEffect(() => {
    const fetchProfileImage = async () => {
      if (!!profileImageId) {
        try {
        const profileImageUrl = buildImageUrl(id, profileImageId);
        if (profileImageUrl) {
          setProfileImage(profileImageUrl);
        } else {
          setProfileImage("/profile_placeholder.png");
        }
      } catch (error) {
        console.error("error", error);
      }
      }
      
    };
    fetchProfileImage();
  }, []);

  return (
    <Card
      sx={{ width: "100%", borderRadius: 2 }}
      style={{
        overflow: "auto",
        // boxShadow: `0 4px 8px rgba(0, 0, 0, 0.2)`,
        border: `1px solid #679289`,
      }}
    >
      <Link to={linkUrl} style={{ textDecoration: "none", color: "inherit" }}>
        <CardMedia
          sx={{ height: 265, width: "auto", objectFit: "cover" }}
          image={profileImage}
        />
      </Link>
      <CardContent style={{ padding: "16px", color: "#003554" }}>
        <Typography
          gutterBottom
          variant="h5"
          component="div"
          style={{ fontWeight: "bold" }}
        >
          {name}
        </Typography>
        <Typography variant="body1" color="#679289">
          Age: {age}
        </Typography>
        <Typography variant="body1" color="#679289">
          Breed: {breed}
        </Typography>
        <Typography variant="body1" color="#679289">
          Location: {location}
        </Typography>
      </CardContent>
      <CardActions style={{ justifyContent: "center" }}>
        {/* <a href={linkUrl} style={{ textDecoration: "none" }}> */}
        <Link to={linkUrl} style={{ textDecoration: "none", color: "inherit" }}>
          <Button
            variant="contained"
            sx={{
              fontFamily: "Arial, sans-serif",
              backgroundColor: "#003554",
              color: "#FFFACA",
              "&:hover": {
                backgroundColor: "#557B71",
                marginRight: "1em",
                marginLeft: "1em",
              },
            }}
          >
            {button1Text}
          </Button>
        </Link>
      </CardActions>
    </Card>
  );
};
// Define the prop types for the component
AnimalCard.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  age: PropTypes.number.isRequired,
  breed: PropTypes.string.isRequired,
  location: PropTypes.string.isRequired,
  profileImageId: PropTypes.string,
  button1Text: PropTypes.string,
  linkUrl: PropTypes.string.isRequired,
  shelter_id: PropTypes.number.isRequired,
};

export default AnimalCard;

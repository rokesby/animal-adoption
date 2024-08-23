import { Link } from "react-router-dom";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";

const AnimalCard = ({
  name,
  age,
  breed,
  location,
  image,
  button1Text,
  linkUrl,
}) => {


  const placeholderImage = "https://placecats.com/265/265";
  const specificSubstring = "unique_id";
  const realImage = image && !image.includes(specificSubstring)
    ? `${import.meta.env.VITE_BACKEND_URL}/upload/${image}`
    : placeholderImage;
  // const realImage = import.meta.env.VITE_BACKEND_URL + "/upload/" + image;

  return (
    <Card
      sx={{ maxWidth: 380, borderRadius: 2 }}
      style={{
        margin: "2em",
        overflow: "hidden",
        boxShadow: `0 4px 8px rgba(0, 0, 0, 0.2)`,
        border: `1px solid #679289`,
      }}
    >
      <Link to={linkUrl} style={{ textDecoration: "none", color: "inherit" }}>
        <CardMedia
          sx={{ height: 265, width: "100%", objectFit: "cover" }}
          image={realImage || placeholderImage}
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
        <a href={linkUrl} style={{ textDecoration: "none" }}>
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
        </a>
      </CardActions>
    </Card>
  );
};
// Define the prop types for the component
AnimalCard.propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number.isRequired,
  breed: PropTypes.string.isRequired,
  location: PropTypes.string.isRequired,
  image: PropTypes.string,
  button1Text: PropTypes.string,
  linkUrl: PropTypes.string.isRequired,
};

export default AnimalCard;

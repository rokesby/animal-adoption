import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import PropTypes from 'prop-types'; 

const dummyImage = "https://via.placeholder.com/265"; // Dummy image URL

const AnimalCard = ({ name, age, breed, location, image, button1Text, linkUrl }) => {
  return (
    <Card sx={{ maxWidth: 380 }} style={{ margin: "2em", overflow: "hidden" }}>
      <CardMedia
        sx={{ height: 265, width: "100%", objectFit: "cover" }}
        image={image || dummyImage} 
      />

<CardContent data-testid="animal-card">
        <Typography gutterBottom variant="h5" component="div">
          {name}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Age: {age}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Breed: {breed}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Location: {location}
        </Typography>
      </CardContent>
      <CardActions style={{ justifyContent: "center" }}>
        <a href={linkUrl} style={{ textDecoration: 'none' }}>
          <Button variant="outlined">{button1Text}</Button>
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
  linkUrl: PropTypes.string.isRequired
};

export default AnimalCard;

import React from "react";
import PropTypes from "prop-types";

// The parameter of this function is an object with a number called num_likes
// and a bool called lognameLikesThis inside it.
// num_likes is a prop for the like button component.
export default function LikeButton({ lognameLikes, numLikes, onUpdate }) {
  /* Display like button and number of likes of a single post */

  // Render like/unlike button and num likes
  return (
    <div className="likeButton">
      <button data-testid="like-unlike-button" type="button" onClick={onUpdate}>
        {lognameLikes ? "unlike" : "like"}
      </button>
      {numLikes === 1 ? <p> 1 like </p> : <p> {numLikes} likes </p>}
    </div>
  );
}

LikeButton.propTypes = {
  lognameLikes: PropTypes.bool.isRequired,
  numLikes: PropTypes.number.isRequired,
  onUpdate: PropTypes.func.isRequired,
};

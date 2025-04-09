import React from "react";
import PropTypes from "prop-types";

// The parameter of this function is an object with a string called text
// and a string called owner inside it.
// text and owner are props for the comment component.
export default function Comment({ comment, onDelete }) {
  /* Display comments of a single post */

  // Render comments and textfield
  return (
    <div className="comments">
      <a href={comment.ownerShowUrl}> {comment.owner} </a>
      <span data-testid="comment-text"> {comment.text} </span>
      {comment.lognameOwnsThis && (
        <button
          data-testid="delete-comment-button"
          type="button"
          onClick={() => onDelete(comment)}
        >
          Delete Comment
        </button>
      )}
    </div>
  );
}

Comment.propTypes = {
  comment: PropTypes.shape({
    commentid: PropTypes.number,
    lognameOwnsThis: PropTypes.bool,
    owner: PropTypes.string,
    ownerShowUrl: PropTypes.string,
    text: PropTypes.string,
    url: PropTypes.string,
  }).isRequired,
  onDelete: PropTypes.func.isRequired,
};

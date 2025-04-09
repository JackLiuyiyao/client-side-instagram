import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import Comment from "./comment";
import LikeButton from "./like_button";

dayjs.extend(relativeTime);
dayjs.extend(utc);

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [created, setCreated] = useState("");
  const [postidUrl, setPostidUrl] = useState("");
  const [postid, setPostId] = useState(0);
  const [likeUrl, setLikeUrl] = useState("");
  const [numLikes, setNumLikes] = useState(0);
  const [lognameLikesPost, setLognameLikesPost] = useState(false);
  const [comments, setComments] = useState([]); // set comments to an array and not a string
  const [textEntry, setTextEntry] = useState("");
  const [fetchDone, setFetchDone] = useState(false);


  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    setFetchDone(false);

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          setOwnerImgUrl(data.ownerImgUrl);
          setOwner(data.owner);
          setCreated(data.created);
          setPostidUrl(data.postShowUrl);
          setComments(data.comments);
          setPostId(data.postid);
          setNumLikes(data.likes.numLikes);
          setLikeUrl(data.likes.url);
          setLognameLikesPost(data.likes.lognameLikesThis);
          setFetchDone(true);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url, numLikes]);

  // humanize timestamp
  let utc = dayjs(created).utc(true);
  let humanize = dayjs(utc).toNow(true);

  const likeUnlike = () => {
    if (lognameLikesPost) {
      console.log("unliking");
      fetch(likeUrl, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        method: "DELETE",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
        })
        .then(() => {
          setNumLikes(numLikes - 1);
          setLognameLikesPost(false);
        })
        .catch((error) => console.log(error));
    } else {
      const postLikeUrl = `/api/v1/likes/?postid=${postid}`;
      fetch(postLikeUrl, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        method: "POST",
        body: JSON.stringify({
          postid: postid,
        }),
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          setNumLikes(numLikes + 1);
          setLognameLikesPost(true);
          setLikeUrl(data.url);
        })
        .catch((error) => console.log(error));
    }
  };

  const handleDoubleClick = () => {
    if (!lognameLikesPost) {
      const postLikeUrl = `/api/v1/likes/?postid=${postid}`;
      fetch(postLikeUrl, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        method: "POST",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          console.log(data);
          setNumLikes(numLikes + 1);
          setLognameLikesPost(true);
          setLikeUrl(data.url);
        })
        .catch((error) => console.log(error));
    }
  };

  const handleChange = (event) => {
    setTextEntry(event.target.value);
  };

  const addComment = (event) => {
    const commentUrl = `/api/v1/comments/?postid=${postid}`;
    fetch(commentUrl, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        text: textEntry,
      }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setTextEntry("");
        setComments(comments.concat(data));
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  };

  const deleteComment = (comment) => {
    fetch(comment.url, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .then(() =>
        setComments((oldValues) => oldValues.filter((c) => c !== comment)),
      )
      .catch((error) => console.log(error));
  };

  // Render post
  return (
    <div className="post">
      {fetchDone ?
        (
          <>
            <p>{owner}</p>
            <img style={{ width: 50, height: 60 }} src={ownerImgUrl} alt="ownerimage" />
            <img src={imgUrl} alt="post_image" onDoubleClick={handleDoubleClick} />
            <a href={postidUrl}> {humanize}</a>
            <LikeButton
              numLikes={numLikes}
              lognameLikes={lognameLikesPost}
              onUpdate={likeUnlike}
            />
            {comments.map((comment) => (
              <Comment key={comment.commentid} comment={comment} onDelete={deleteComment} />
            ))}
            <form data-testid="comment-form" onSubmit={addComment}>
              <input type="text" value={textEntry} onChange={handleChange} />
            </form>
          </>
        ) : (<p> Loading </p>)
      }
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

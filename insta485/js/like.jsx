import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";


dayjs.extend(relativeTime);
dayjs.extend(utc);


// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Like({ url }) {
  /* Display image and post owner of a single post */

  const [likeid, setLikeStatus] = useState([]);

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url,{ credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setLikeStatus(data.likeid);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

 
  

  // Render post image and post owner
  return (
    <div className="like">
      Hello There
   
    </div>
  );
}

Like.propTypes = {
  url: PropTypes.string.isRequired,
};

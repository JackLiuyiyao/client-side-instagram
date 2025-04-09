import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "./post";

export default function Feed() {
  /* Display feed of posts */

  const [posts, setPosts] = useState([]);
  const [next, setNext] = useState("/api/v1/posts/"); // next url, update will trigger next effect
  const [tempnext, setTempnext] = useState(""); // temporary store next before triggering next effect
  const [hasMore, setHasMore] = useState(true); // weather there are still more posts
  useEffect(() => {
    // append ten more posts to the page

    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(next, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setPosts([...posts, ...data.results]); // concat the next 10 posts
          setTempnext(data.next);
          if (!data.next) {
            setHasMore(false);
          }
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Feed component
      // unmounts or re-renders. If a Feed is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [next]);

  // Render the posts
  return (
    <div className="feed">
      <InfiniteScroll
        dataLength={posts.length}
        next={() => setNext(tempnext)}
        hasMore={hasMore}
        loader={<h4>Loading...</h4>}
        endMessage={
          <p style={{ textAlign: "center" }}>
            <b>No more post avaliable</b>
          </p>
        }
        scrollThreshold={1}
      >
        {posts.map((post) => (
          <Post key={post.postid} url={post.url} />
        ))}
      </InfiniteScroll>
    </div>
  );
}

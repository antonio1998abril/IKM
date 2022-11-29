import FadeLoader from "react-spinners/FadeLoader";

function Loading() {
  return (
    <div className="sweet-loading ">
      <FadeLoader
        color="#36d7b7"
        size={250}
        aria-label="Loading Spinner"
        data-testid="loader"
      />
    </div>
  );
}

export default Loading;

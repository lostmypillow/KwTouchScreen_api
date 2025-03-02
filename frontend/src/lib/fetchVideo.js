export async function fetchVideo(currentVideoIndex) {
  const response = await fetch(
    import.meta.env.VITE_SERVER_URL + "/video/play/" + currentVideoIndex
  );
  return URL.createObjectURL(await response.blob());
}

export async function fetchAutoWatchlist() {
  const res = await fetch("http://localhost:8008/autowatchlist", {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch autowatchlist");
  }

  return res.json();
}

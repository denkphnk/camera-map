import { Navigate, useParams } from "react-router-dom";

export function LocationPage() {
  const { id } = useParams();

  return (
    <Navigate
      to={`/cameras/${id}`}
      replace
    />
  );
}
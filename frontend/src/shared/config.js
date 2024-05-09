export default Object.freeze({
  HOSTNAME: function () {
    //TODO use dev or prod env var
    return "http://localhost:8080/";
  },
  API_HOSTNAME: function () {
    //TODO use dev or prod env var
    return "http://localhost:8000/";
  },
  BASE_API_V1_URL: "api/v1/",
});

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">{{ sotwName }}</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="offcanvas offcanvas-end" tabindex="-1" id="navbarSupportedContent" aria-labelledby="navbarOffcanvasLgLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">{{ sotwName }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <!-- <li class="nav-item">
              <a class="nav-link" href="#">About</a>
            </li> -->
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarResultsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Results
              </a>
              <ul class="dropdown-menu" aria-labelledby="navbarResultsDropdown">
                <li><a class="dropdown-item" href="#">This Week's Results</a></li>
                <li><a class="dropdown-item" href="#">Previous Results</a></li>
              </ul>
            </li>
            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/">Data</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/">Playlists</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/">Rules</a>
            </li>
            <!-- <li class="nav-item">
              <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
            </li> -->
          </ul>
          <div class="navbar-nav d-flex">
            <div class="nav-item">
              <button class="btn btn-outline-success" href="#">Sign In</button>
            </div>
          </div>
          <!-- <form class="d-flex">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form> -->
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  props: {
    sotwName: {
      type: String,
      defualt: "Song of the Week",
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>

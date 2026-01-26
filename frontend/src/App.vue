<script setup>

import { RouterLink } from 'vue-router';
</script>

<template>
  <div id="appStyle">
    <nav class="navbar navbar-expand-md bg-body py-3" style="box-shadow: 0px 0px 10px 5px;">
            <div class="container"><a class="navbar-brand d-flex align-items-center" href="#">
              <span><router-link to="/" class="a-router">Final Year Project 2025</router-link></span>
                </a>
                <div class="collapse navbar-collapse flex-grow-0 order-md-first" id="navcol-4">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item"></li>
                        <li class="nav-item"></li>
                    </ul>
                    <div class="d-md-none my-2"><button class="btn btn-light me-2" type="button">Button</button><button class="btn btn-primary" type="button">Button</button></div>
                </div>
                <div class="d-none d-md-block"></div>
            </div>
        </nav>
  <router-view />
  </div>
</template>

<script>
export default {
  computed: {
    backgroundImage() {
      switch (this.$route.name) {
        case 'home':
          return 'url("./src/assets/bg1.jpg")'; 
        case 'laptopinfo':
          return 'url("./src/assets/bg2.jpg")'; 
        case 'recommend':
          return 'url("./src/assets/bg3.jpg")';
        default:
          return 'url("./src/assets/bg1.jpg")'; 
      }
    },
  },
};
</script>

<style>
  #appStyle {
    background-image: v-bind(backgroundImage); 
    background-size: cover;
    background-position: center;
    min-height: 100vh;
  }
  .a-router{
    text-decoration: none;
    color: black;
    font-family: ABeeZee, sans-serif;
  }
</style>

<style scoped>
  
</style>



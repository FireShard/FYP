<template>
        <div class="pb-0 mb-5"></div>
        <section class="text-center py-4 py-xl-5 pb-1 mb-0" style="background: rgba(230,230,230,0.3);">
            <div class="container h-100">
                <div class="row h-100">
                    <div class="col-md-10 col-xl-8 text-center d-flex d-sm-flex d-md-flex justify-content-center align-items-center mx-auto justify-content-md-start align-items-md-center justify-content-xl-center">
                        <div>
                            <h2 class="text-uppercase fw-bold mb-3"><strong><span style="color: rgb(0, 0, 0);">LAPTOP AND RAM COMPATIBILITY CHECKER AND RECOMMENDATION&nbsp;</span></strong></h2>
                            <p class="mb-4">A website that checks for compatibility between your laptop's RAM type and a RAM that you would like to buy. This website also recommends RAM that are compatible with you laptop.</p>
                            <button class="btn btn-primary fs-5 me-2 py-2 px-4" type="button" @click="goToLaptopInfo">Input Laptop Information</button>
                        </div>
                    </div>
                </div>
            </div>
            <div></div>
        </section>
</template>

<script>
    export default{
        name: "Home",
        methods: {
            goToLaptopInfo(){
                this.$router.push("/laptopinfo");
            }
        }
    };
</script>

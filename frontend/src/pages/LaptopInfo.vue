<template>
    <body style="background: url(&quot;assets/img/Aboutme.jpg&quot;) center / cover;">
        <div class="text-center mb-0 pb-0 mt-0 pt-5" style="padding-top: 150px;">
        <h1 class="mb-5">Enter Your Laptop Information</h1>
        <form class="pe-3 ms-0 ps-3" @submit.prevent="predictRamType">
            <div class="row" style="background: rgba(230,230,230,0.3);">
                <div class="col-xl-1"></div>
                <div class="col"><label class="form-label" style="font-family: ABeeZee, sans-serif;">Manufacturer</label><select class="form-select" v-model="manufacturer">
                        <option value="Acer">Acer</option>
                        <option value="Asus">Asus</option>
                        <option value="Avita">Avita</option>
                        <option value="Dell">Dell</option>
                        <option value="HP">HP</option>
                        <option value="Lenovo">Lenovo</option>
                        <option value="MSI">MSI</option>
                    </select></div>
                <div class="col"><label class="form-label" style="font-family: ABeeZee, sans-serif;">CPU Brand (Intel,AMD)</label><select class="form-select" v-model="CPUbrand" id="CPUbrand">
                        <option value="Intel">Intel</option>
                        <option value="AMD">AMD</option>
                    </select></div>
                <div class="col-xl-1"></div>
            </div>
            <div class="row" style="background: rgba(230,230,230,0.3);">
                <div class="col-xl-1"></div>
                <div class="col-xl-5"><label class="form-label" style="font-family: ABeeZee, sans-serif;">Current RAM Size (GB)</label><select class="form-select" v-model="ramSize">
                        <option value="4">4GB</option>
                        <option value="8">8GB</option>
                        <option value="16">16GB</option>
                        <option value="32">32GB</option>
                    </select></div>
                <div class="col"><label class="form-label" style="font-family: ABeeZee, sans-serif;">CPU Name</label><select class="form-select" v-model="CPUName" id="CPUName">
                        <option value="Core i3" v-if="CPUbrand === 'Intel'">Core i3</option>    
                        <option value="Core i5" v-if="CPUbrand === 'Intel'">Core i5</option>
                        <option value="Core i7" v-if="CPUbrand === 'Intel'">Core i7</option>
                        <option value="Core i9" v-if="CPUbrand === 'Intel'">Core i9</option>
                        <option value="Ryzen 3" v-if="CPUbrand === 'AMD'">Ryzen 3</option>
                        <option value="Ryzen 5" v-if="CPUbrand === 'AMD'">Ryzen 5</option>
                        <option value="Ryzen 7" v-if="CPUbrand === 'AMD'">Ryzen 7</option>
                        <option value="Ryzen 9" v-if="CPUbrand === 'AMD'">Ryzen 9</option>
                    </select></div>
                <div class="col-xl-1"></div>
            </div>
            <div class="row" style="background: rgba(230,230,230,0.3);">
                <div class="col-xl-1"></div>
                <div class="col"><label class="form-label" style="font-family: ABeeZee, sans-serif;">System Architecture</label><select class="form-select" v-model="architecture">
                        <option value="32-bit">32-bit</option>
                        <option value="64-bit">64-bit</option>
                    </select></div>
                <div class="col"><label class="form-label" style="font-family: ABeeZee, sans-serif;">CPU Generation</label><select class="form-select" v-model="CPUGen" id="CPUGen">
                        <option value="7th" v-if="CPUbrand === 'Intel'">7th Generation</option>
                        <option value="8th" v-if="CPUbrand === 'Intel'">8th Generation</option>
                        <option value="9th" v-if="CPUbrand === 'Intel'">9th Generation</option>
                        <option value="10th" v-if="CPUbrand === 'Intel'">10th Generation</option>
                        <option value="11th" v-if="CPUbrand === 'Intel'">11th Generation</option>
                        <option value="12th" v-if="CPUbrand === 'Intel'">12th Generation</option>
                        <option value="Not Available" v-if="CPUbrand === 'AMD'">Not Available</option>
                    </select></div>
                <div class="col-xl-1"></div>
            </div><button class="btn btn-primary btn-lg mt-2 me-3" type="submit">Submit</button>
        </form>
    </div>
</body>
</template>

<script>
import axios from "axios";

export default{
        name: "LaptopInfo",
        data(){
            return{
                manufacturer: "",
                ramSize: "",
                architecture: "",
                CPUbrand: "",
                CPUName: "",
                CPUGen: "",
                ramType: "",
                ramid: "1"
            }
        },

        methods: {
            addUserLaptop(){
                const newUserLaptop = {
                    manufacturer: this.manufacturer,
                    ramSize: this.ramSize,
                    architecture: this.architecture,
                    CPUbrand: this.CPUbrand,
                    CPUName: this.CPUName,
                    CPUGen: this.CPUGen,
                    ramType: this.ramType,
                    ramid: this.ramid
                };

                axios
                    .post("http://127.0.0.1:8000/UserLaptop/", newUserLaptop)
                    .then(response => {
                        console.log("Added Laptop Details Successfully", response.data);
                        alert("Added Laptop Details Successfully!");
                        this.goToRecommend();
                    })
                    .catch((error) =>{
                        console.error("Error in saving laptop data", error);
                        alert("Failed in saving laptop data. Please try again");
                    })     
            },
            goToRecommend(){
                this.$router.push({ 
                    path: '/recommend', 
                    query: { 
                    manufacturer: this.manufacturer, 
                    ramSize: this.ramSize, 
                    architecture: this.architecture, 
                    CPUbrand: this.CPUbrand, 
                    CPUName: this.CPUName, 
                    CPUGen: this.CPUGen, 
                    ramType: this.ramType 
                    } 
                });
            },

            async predictRamType() {
                try {

                    const response = await axios.post('http://127.0.0.1:8000/predictRAMType/',{
                        processor_brand: this.CPUbrand,
                        processor_name: this.CPUName,
                        processor_gnrtn: this.CPUGen,
                        os_bit: this.architecture,
                        brand: this.manufacturer,
                        ram_gb: this.ramSize,
                    });

                    console.log('Received data:', response.data);
                    this.ramType = response.data;
                    this.error = null;
                    console.log("RAM Type Predicted Successfully", response.data);
                    alert("RAM Type Predicted Successfully!");
                    this.goToRecommend();
                } 
                catch (error) {
                    console.error('Error predicting RAM type:', error);
                    this.ramType = 'Prediction Failed';
                    alert("Failed in predicting RAM type. Please try again");
                }
            },
        },
}
</script>
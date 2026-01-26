<template>
<body style="background: url(&quot;assets/img/Aboutmev2.jpg&quot;);background-size: cover;">
    <div class="text-center pb-0 mb-5">
        <h1 class="mt-5">Your Compatible RAM Type:&nbsp;</h1>
        <h1 style="color: #5bdc3b;font-size: 50px;background: rgba(241,241,241,0.35);">{{ receivedData.ramType }}</h1>
    </div>
    <form class="pb-0 mb-3" @submit.prevent="findCompatibleRAM">
        <div class="row">
            <div class="col">
                <div class="row">
                    <div class="col-3 offset-xl-0"></div>
                    <div class="col text-center">
                        <label class="form-label" style="font-family: ABeeZee, sans-serif;">Got a Shopee link? Paste here to check for compatiblity!</label><input class="form-control" type="text" v-model="ramLink">
                        <button class="btn btn-primary" type="submit" style="background: rgb(255,255,255);color: rgb(0,0,0);font-family: ABeeZee, sans-serif;">Check!</button></div>
                    <div class="col-3"></div>
                </div>
            </div>
        </div>
    </form>
    <p style="text-align: center;font-family: ABeeZee, sans-serif;">Here are compatible RAMs that you can buy from Shopee:</p>
    <div>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>RAM Brand</th>
                        <th>Shopee Link</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="compatibleRAMList in filteredRAMs" :key="compatibleRAMList.id">
                        <td>{{ compatibleRAMList.shopeeListing }}</td>
                        <td>{{ compatibleRAMList.ramLink }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</template>

<script>
    import axios from "axios";

    export default{
        name: "Recommend",
        data() {
            return {
                receivedData: {},
                ramData: [],
                ramLink: "",
                error: null,
                compatibleRAMList: [],
            };
        },

        created() {
            // Debug pruposes
            this.receivedData = this.$route.query;
            console.log('Received data:', this.$route.query);
        },

        

        UserLapData(){
            return{
                userLaptop:{
                    manufacturer: "",
                    ramSize: "",
                    architecture: "",
                    CPUbrand: "",
                    CPUName: "",
                    CPUGen: "",
                    ramType: "",
                }
            }
        },

        mounted(){
            this.fetchRamDetails();
        },

        computed:{
            filteredRAMs() {
            return this.compatibleRAMList;
        }
        },

        methods:{
            async fetchRamDetails() {
                try {
                    const response = await axios.get("http://127.0.0.1:8000/RamDetails");

                    // Log success to the console
                    console.log("RAM Data fetched successfully:", response.data);

                    // Assuming 'UserLapData' is the correct field from the response
                    this.ramData = response.data;
                    this.filterCompatbleRAM();

                } catch (err) {
                    // Log error message to the console
                    this.error = "Failed to fetch User RAM Data";
                    console.error("Error fetching data:", err);
                }
            },

            async findCompatibleRAM(){
                try {
                    const response = await axios.post('http://127.0.0.1:8000/predictCompatibility/',{
                        word1: this.$route.query.ramType,
                        word2: this.ramLink,
                    });

                    console.log('RAM Type Sent:', this.$route.query.ramType);
                    console.log('Received data:', response.data);
                    this.error = null;
                    console.log("RAM Compatibility Predicted Successfully!", response.data);
                    alert(response.data);

                } catch (err) {
                    // Log error message to the console
                    this.error = "Failed to fetch User Laptop Data";
                    console.error("Error fetching data:", err);
                }
            },

            async filterCompatbleRAM() {
                try {
                    const ramDetailList = this.ramData;/* Your data source for RAM details */ //  This should be an array of objects
                    const compatibleRAM = [];
                    const results = []; // Array to store results for each RAM link

                    for (const ramDetails of ramDetailList) {
                        const ramLink = ramDetails.ramLink; // Access the ramLink from each item in the array

                        const response = await axios.post('http://127.0.0.1:8000/predictCompatibility/', {
                            word1: this.$route.query.ramType,
                            word2: ramLink,
                        });

                        console.log('RAM Type Sent:', this.$route.query.ramType);
                        console.log('RAM Link Sent:', ramLink);
                        console.log('Received data:', response.data);

                        // Check for compatibility and add to the filtered list
                        if (response.data.includes("Compatible")) { // Improved compatibility check
                            compatibleRAM.push(ramDetails); // Store the entire ramDetail object
                        }

                        console.log("RAM Compatibility Predicted:", response.data);
                    }

                    this.error = null;

                    console.log("Compatible RAM Details:", compatibleRAM);

                    this.compatibleRAMList = compatibleRAM; // Store the filtered list in a data property

                } catch (err) {
                    this.error = "Failed to fetch RAM Compatibility Data";
                    console.error("Error fetching data:", err);
                }
                },
        }
    }
</script>
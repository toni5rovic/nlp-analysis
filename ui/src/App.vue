<template>
  <v-app id="inspire">
    <v-app-bar app clipped-right class="teal darken-1" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>NLP - Final Practice</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" class="teal lighten-5" relative app>
      <v-list dense>
        <v-list-item @click.stop="showModal=true">
          <v-list-item-action>
            <v-icon>mdi-plus</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>New Analysis</v-list-item-title>
          </v-list-item-content>
           <Modal v-model="showModal" :loadText="loadText"/>
        </v-list-item>
        
        <v-divider></v-divider>

        <v-list-item @click.stop="originalText">
          <v-list-item-action>
            <v-icon>mdi-text</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>View Original Text</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item @click.stop="disambiguationAnalysis">
          <v-list-item-action>
            <v-icon>mdi-call-split</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Disambiguation</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click.stop="synonymAnalysis">
          <v-list-item-action>
            <v-icon>mdi-equal</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Synonyms</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click.stop="antonymAnalysis">
          <v-list-item-action>
            <v-icon>mdi-minus</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Antonyms</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item @click.stop="morphologicalAnalysis">
          <v-list-item-action>
            <v-icon>mdi-chart-pie</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Morphological analysis</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item @click.stop="nerAnalysis">
          <v-list-item-action>
            <v-icon>mdi-more</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Named Entity Recognition</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <v-container class="fill-height" fluid>
        <v-row class="ma-7">
          <v-col class="fill-height pa-6">
            <div v-if="loading == true" >
               <v-progress-circular indeterminate color="primary" size="75">
               </v-progress-circular>
            </div>
            <div v-else-if="currentAnalysis == null && loading==false">
              {{textToProcess}}
            </div>
            <div v-else-if="currentAnalysis == 'morphological' && loading==false"> 
              <Statistics :statistics="statistics"/>
            </div>
            <div v-else-if="loading==false">
              <span v-for="partsArray in results.sentList" :key="partsArray.id">
                <span v-for="partWithTag in partsArray.sentence" :key="partWithTag.id">
                  <span v-if="partWithTag.tags == null">{{partWithTag.part}}</span>
                  <v-tooltip v-else top color="blue-grey darken-3">
                    <template v-slot:activator="{ on }">
                      <v-chip color="indigo" text-color="white" small v-on="on" class="mb-1">
                        <v-avatar v-if="currentAnalysis == 'NER'" small left class="indigo darken-2"> 
                          <v-icon small v-if="partWithTag.tags == 'PERSON'">mdi-account-circle</v-icon>
                          <v-icon small v-else-if="partWithTag.tags == 'ORGANIZATION'">mdi-domain</v-icon>
                          <v-icon small v-else-if="partWithTag.tags == 'LOCATION'">mdi-map-marker</v-icon>
                          <v-icon small v-else-if="partWithTag.tags == 'GPE'">mdi-crosshairs-gps</v-icon>
                        </v-avatar>
                        {{partWithTag.part}}
                      </v-chip>
                    </template>
                    <span>
                      <ul>
                        <li v-for="tag in partWithTag.tags" :key="tag">
                          {{tag}}
                        </li>
                      </ul>
                    </span>
                  </v-tooltip>
                  
                </span>
                {{spaceCharacter}}
              </span>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-content>

    <v-footer app class="teal darken-1 white--text">
      <span>NLP - Antonije Petrovic</span>
      <v-spacer></v-spacer>
      <span>2020</span>
    </v-footer>
  </v-app>
</template>

<script>
  import Modal from './components/Modal'
  import Statistics from './components/Statistics'
  export default {
    name: 'App', 
    components: { 
      Modal,
      Statistics
    },
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
      showModal: false,
      textToProcess: null,
      results: null,
      currentAnalysis: null,
      statistics: null,
      spaceCharacter: " ",
      loading: false
    }),
    methods: {
      loadText(txt) {
        this.textToProcess = txt
        this.results = null
        this.currentAnalysis = null
      },
      originalText() {
        this.results = null
        this.currentAnalysis = null
      },
      disambiguationAnalysis() {
        if (this.textToProcess != null) {
          //this.sendRequest("semantic", this.textToProcess, "disambiguation")
          this.sendPostRequest("semantic", this.textToProcess, "disambiguation")
          this.currentAnalysis = "disambiguation"
        }
      },
      synonymAnalysis() {
        if (this.textToProcess != null) {
          this.sendPostRequest("semantic", this.textToProcess, "synonyms")
          this.currentAnalysis = "synonyms"
        }
      },
      antonymAnalysis() {
        if (this.textToProcess != null) {
          this.sendPostRequest("semantic", this.textToProcess, "antonyms")
          this.currentAnalysis = "antonyms"
        }
      },
      nerAnalysis() {
        if (this.textToProcess != null) {
          this.sendPostRequest("NER", this.textToProcess)
          this.currentAnalysis = "NER"
        }
      },
      morphologicalAnalysis() {
        if (this.textToProcess != null) {
          this.sendPostStatisticsRequest(this.textToProcess)
          this.currentAnalysis = "morphological"
        }
      },
      sendRequest(typeOfAnalysis, text, typeOfSemanticAnalysis=null) {
        this.loading = true
        let url = 'http://localhost:5000/api/analysis/' + typeOfAnalysis + "?text=" + encodeURI(text)
        if (typeOfSemanticAnalysis != null) {
          url += '&type=' + typeOfSemanticAnalysis
        }

        var vm = this;
        fetch(url, {
          method: 'get'
        })
        .then((response) => {
          return response.json()
        })
        .then((jsonData) => {
          let res = JSON.parse(JSON.stringify(jsonData))
          vm.results = res
        })

        this.loading = false
      },
      sendPostRequest(typeOfAnalysis, text, typeOfSemanticAnalysis=null) {
        this.loading = true
        let url = 'http://localhost:5000/api/analysis/' + typeOfAnalysis
        let requestBody = {
          "text": text,
          "type": typeOfSemanticAnalysis
        }

        var vm = this;
        fetch(url, {
          method: 'post',
          mode: 'cors', // no-cors, *cors, same-origin
          headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: JSON.stringify(requestBody) // body data type must match "Content-Type" header
        })
        .then((response) => {
          return response.json()
        })
        .then((jsonData) => {
          let res = JSON.parse(JSON.stringify(jsonData))
          vm.results = res
        })
        this.loading = false
      },
      sendPostStatisticsRequest(text) {
        this.loading = true
        let url = 'http://localhost:5000/api/analysis/morphological'
        let requestBody = {
          "text": text
        }

        var vm = this;
        fetch(url, {
          method: 'post',
          mode: 'cors', // no-cors, *cors, same-origin
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestBody) // body data type must match "Content-Type" header
        })
        .then((response) => {
          return response.json()
        })
        .then((jsonData) => {
          let stat = JSON.parse(JSON.stringify(jsonData))
          vm.statistics = stat
        })
        this.loading = false
      },
      process(partWithTag) {
        return partWithTag.part
      }
    }
  }
</script>
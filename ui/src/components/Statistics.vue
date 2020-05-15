<template>
    <div v-if="statistics != null">
        <!-- <v-content> -->
            <v-container >
                <v-row class="">
                    <v-col>
                        <v-card class="mx-auto ma-2" max-width="344" >
                            <v-card-text>
                                <div class="title text--primary">
                                    Morphological analysis
                                </div>
                                <v-divider></v-divider>
                                <div class="subtitle text--primary">
                                    Number of sentences: {{statistics.sentsNum}}
                                </div>
                                
                                <v-divider></v-divider>
                                
                                <div class="subtitle text--primary">
                                    Number of tokens: {{statistics.tokensNum}}
                                </div>
                                <div class="subtitle text--primary">
                                    Unique tokens number: {{statistics.tokensUniqueNum}}
                                </div>
                                <div class="subtitle text--primary">
                                    Number of stopwords: {{statistics.stopwordsNum}}
                                </div>
                                <div class="subtitle text--primary">
                                    Number of unique stopwords: {{statistics.stopwordsUniqueNum}}
                                </div>
                                
                                <v-divider></v-divider>

                                <div class="subtitle text--primary">Number of nouns: {{statistics.nounsNum}}</div>
                                <div class="subtitle text--primary">Number of verbs: {{statistics.verbsNum}}</div>
                                <div class="subtitle text--primary">Number of adjectives: {{statistics.adjsNum}}</div>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col>
                        <v-card class="mx-auto ma-2" max-width="344" >
                            <v-card-text>
                                <div class="title text--primary">
                                Top 5 words and their frequencies
                                </div>
                                <v-list dense>
                                    <v-list-item-group color="primary">
                                        <v-list-item v-for="(wordFreqPair, i) in statistics.top5Words" :key="i">
                                            <v-list-item-content>
                                                <v-list-item-title>{{wordFreqPair[0]}} : {{wordFreqPair[1]}}</v-list-item-title>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-list-item-group>
                                </v-list>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        <!-- </v-content> -->
    </div>
</template>

<script>
export default {
  name: 'Statistics',
  props: ['statistics']  
};
</script>
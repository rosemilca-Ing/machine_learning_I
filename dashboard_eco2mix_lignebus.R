# remove.packages("ggplot2") # Unisntall ggplot
#install.packages("ggplot") # Install it again
install.packages("mongolite")
library(mongolite)
library(shiny)
library(shinydashboard)
library(DT)
library(ggplot2)
library(Hmisc)
library(UsingR)


shinyApp(
  ui = dashboardPage(
    skin = "blue",
    dashboardHeader(
      titleWidth =300,
      title = "Eco2mix & Ligne Bus"
    ),
    dashboardSidebar(
      width = 300,
      sidebarMenu(
        menuItem(text = "Ligne bus", tabName = "vue1", icon = icon("bus")),
        menuItem(text = "Eco2mix", tabName = "vue2", icon = icon("bolt"))
      )
    ),
    dashboardBody(
      tags$style(HTML(".sidebar-menu li a { font-size: 22px; }")),
      
      tabItems(
        tabItem(
          tabName = 
            "vue1",
            h1("Prochains passages des lignes de bus du réseau STAR en temps réel"),
            fluidRow(         
              column(
                4,     
                box(
                  title = "Infos Pratiques",
                  status = "primary",
                  solidHeader = TRUE,
                  width = 12,
                  p(
                    "Nombre Total de lignes de bus : ", 
                    textOutput(outputId ="nbus" ,inline=T), 
                    style = "color: black; font-size: 20px;"
                  ),
                  p(
                    "Nombre Total de bus : ",
                    textOutput("nlbus", inline = T),
                    style = "color: black; font-size: 20px;"
                  ),
                  p(
                    "Nombre Total de destination : ", 
                    style =  "color: black; font-size: 20px",
                    textOutput("nbdestination", inline = T)
                  ),
                ),
              ), 
              column(
                5,
                class = "bg-primary", 
                offset = 1,
                wellPanel(
                  style =  "color: black;",
                  column(
                    6, 
                    # Bouton de recherche du fichier à charger
                    radioButtons(
                      "radio", 
                      label = h3("Choix de (X)"),
                      choices = list("Ligne (ID)" = "idligne", 
                                   "Destination" = "destination", 
                                   "Point d'arrêt (nom)" = "nomarret"), 
                      selected = "destination"
                    ),
                  ),
                  column(
                    6,
                    radioButtons(
                      "radio1", 
                      label = h3("Choix de (Y)"),
                      choices = list("Ligne (ID)" = "idligne", 
                                     "Destination" = "destination", 
                                     "Point d'arrêt (nom)" = "nomarret"), 
                      selected = "idligne"
                    ),
                    hr(),
                  ),
                  fluidRow(
                    column(
                      2,
                      actionButton(inputId = "go", label = "Load")
                    )
                  ),
                ),#wellPanel
              )
            ),#fluid      
            fluidRow(
              #titlePanel("Quantitative vs. Quantitative"),
              mainPanel(
                tabsetPanel(  
                  tabPanel(
                    "Diag. Barres (1 var.)", 
                    fluidRow(
                      column(
                        6,
                        plotOutput("barplotUni")
                      )
                    )
                  ),
                  tabPanel(
                    "Diag. Barres (2 var.)", 
                    fluidRow(
                      column(6, plotOutput("barplotBi")),
                      column(6, plotOutput("barplotDodgeBi"))
                    )
                  ),
                  tabPanel(
                    "Table", 
                    DT::dataTableOutput("table"),
                    style = "font-size: 85%; width:150%;")
                  )
              , style = "font-size: 120%")
            )
        ),
        tabItem(
          tabName = "vue2",
          h1("Données éCO2mix nationales temps réel"),
          column(
            5,
            class = "bg-primary", 
            wellPanel(
              style =  "color: black;",
              column(
                6, 
                # Bouton de recherche du fichier à charger
                radioButtons(
                  "radio3", 
                  label = h3("Choix de (X)"),
                  choices = list("Consommation (MW)" = "consommation", 
                                 "Prévision J-1 (MW)" = "prevision_j1", 
                                 "Taux de CO2 (g/kWh)" = "taux_co2"), 
                  selected = "consommation"
                ),
              ),
              column(
                6,
                radioButtons(
                  "radio4", 
                  label = h3("Choix de (Y)"),
                  choices = list("Consommation (MW)" = "consommation", 
                                 "Prévision J-1 (MW)" = "prevision_j1", 
                                 "Taux de CO2 (g/kWh)" = "taux_co2"), 
                  selected = "prevision_j1"
                ),
                hr(),
              ),
              fluidRow(
                column(
                  2,
                  actionButton(inputId = "go2", label = "Load2")
                )
              ),
            ),#wellPanel
          ),#column
          infoBoxOutput("ibox", width = 5),
          
          #
          fluidRow( 
            
          mainPanel(
            style='margin-top:5%;',
            tabsetPanel(
              tabPanel("Nuage de points", 
                       fluidRow(
                         column(8, offset = 1, plotOutput("nuagePoints"))
                       )
              ), 
             
             
              tabPanel("Caractéristiques", tableOutput("caract")),
              #tabPanel("Tableau", tableOutput("table2"))
              tabPanel(
                "Table", 
                DT::dataTableOutput("table2"),
                style = "font-size: 85%; width:150%;")
            )
          )
          
         )#fluid
          
        )
      )
    ),  
  ),

   server = function(input, output) {
    m <- mongo(collection = "lignebus", db = "eco2mixligne", url = "mongodb://192.168.1.29:27017")
    output$nbus <- renderText({
      length(m$distinct("idligne"))
    })
    output$nlbus <- renderText({
      length(m$distinct("idbus"))
    })
    output$nbdestination <- renderText({
      length(m$distinct("destination"))
    })
    # Recherche et chargement du fichier de données
    data <- eventReactive(input$go, {
      query = m$find()
      df <-as.data.frame(query)
    })

    # Données brutes
    # ----
    output$table <- DT::renderDataTable(
      DT::datatable(
        {data()},
        escape=FALSE,
        options = list(
          autoWidth = TRUE,
          lengthMenu = c(5, 10, 15, 20),
          scrollX = TRUE,
          scrollY = TRUE
        )
      )
    )
    theme_set(
      theme_bw() + theme(
      axis.title = element_text(colour = "blue", face = "bold"),
      plot.title = element_text(colour = "blue", face = "bold"),
      plot.subtitle = element_text(colour = "blue", face = "bold")
      )
    )

    # Diagramme en barres
    # ----
    # Unidimensionnel
    output$barplotUni <- renderPlot({
      choice <-input$radio
      ggplot(data(),
      aes_string(x = choice) ) + geom_bar(shape = 18, linewidth = 1, color = "lightblue", fill="#FF6666")
    })

    # Bidimensionnel
    output$barplotBi <- renderPlot({
      choice <-input$radio
      choice1 <-input$radio1
      # Diagramme en barres entre les variables '
      ggplot(data(), aes_string(x = choice, fill = choice1)) + geom_bar(position = "dodge")
    })

    #vue2
    
    m2 <- mongo(collection = "eco2mix", db = "eco2mixligne", url = "mongodb://192.168.1.29:27017")
    output$ibox <- renderInfoBox({
     # v = m$su
    v= m2$aggregate('[
      { "$match":{"date_heure": {"$gte":"2023-01-01T00:00:00+00"}}},
      { "$group": 
        {
          "_id": null, 
          "nb": {"$sum": "$taux_co2"}
        }
      }
    ]')
    v=v[2]
    
      infoBox(
        title = "Somme des taux de CO2 (g/kWh) en France pour l'année 2023",
        value = paste(v),
        icon = icon("pie-chart"),
        fill = TRUE,
      )
    })
    
    # Recherche et chargement du fichier de données
    data2 <- eventReactive(input$go2, {
      query2 = m2$find()
      df2 <-as.data.frame(query2)
      
    })
    
    
    # ---- # Données brutes
    output$table2 <- DT::renderDataTable(
      DT::datatable(
        {data2()}, 
        escape=FALSE,                   
        options = list(
          autoWidth = TRUE,
          lengthMenu = c(5, 10, 15, 20),
          scrollX = TRUE,
          scrollY = TRUE
        )
      )
    )
    
    # Nuage de points
    # ----
    output$nuagePoints <- renderPlot({
      # Simple nuage de point
      options(scipen=999)
      choice3 <-input$radio3
      choice4 <-input$radio4
      x.var = choice3; y.var = choice4;
      plot(x = data2()[, x.var], y = data2()[, y.var], col = "blue",
           las = 2, cex.axis = 0.7,
           main = paste(y.var, "en fonction de", x.var),
           xlab = x.var, ylab = y.var, cex.lab = 1.2
      )
      options(scipen=0)
    })
    
    # Caractéristiques
    # ----
    output$caract <- renderTable({
      # Définition des colonnes choisies 
      var.names <- c("consommation", "prevision_j1", "taux_co2")
      # Initialisation de la table
      caract.df <- data.frame()
      # Pour chaque colonne, calcul de min, max, mean et ecart-type
      for(strCol in var.names){
        caract.vect <- c(min(data2()[, strCol], na.rm = TRUE), max(data2()[,strCol], na.rm = TRUE), 
                         mean(data2()[,strCol], na.rm = TRUE), sqrt(var(data2()[,strCol], na.rm = TRUE)))
        caract.df <- rbind.data.frame(caract.df, caract.vect)
        print(min(data2()[, strCol]))
      }
      # Définition des row/colnames
      rownames(caract.df) <- var.names
      colnames(caract.df) <- c("Minimum", "Maximum", "Moyenne", "Ecart-type")
      # Renvoyer la table
      caract.df
    }, rownames = TRUE, digits = 0)
  }
)


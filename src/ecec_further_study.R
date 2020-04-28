library(readr)
library(dplyr)
library(string)

# Load data ---------------------------------------------------------------

# Filepath hidden for security reasons
data <- read_csv()


# Remove symbols ----------------------------------------------------------
data <- data %>%
  filter(SurveyYear == "S2019") %>%
  mutate(s_fs_name_v = str_replace_all(s_fs_name_v, "[^[:graph:]]", " "),
         s_fs_name_v = str_replace_all(s_fs_name_v, "[[:punct:]]", ""),
         s_fs_name_v = tolower(s_fs_name_v))



# Fix spelling mistakes ---------------------------------------------------

# Fix common spelling errors for course levels
data <- data %>%
  mutate(s_fs_name_v = gsub("    ", " ", s_fs_name_v),
         s_fs_name_v = gsub("   ", " ", s_fs_name_v),
         s_fs_name_v = gsub("  ", " ", s_fs_name_v),
         
         # Different spellings for bachelor
         s_fs_name_v = gsub("bach ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bacgelor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bachalor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bachelo ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bachelour ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bacherlor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bachleor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bachloer ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bacholer ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bacholor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bahelor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bachlelor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bacholar ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bacholors ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("batchler ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bauchor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bchelor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bechalor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bechlor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("becholar ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("batch of ", "bachelor of ", s_fs_name_v),
         s_fs_name_v = gsub("bachel ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("bachlor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("batchelor ", "bachelor ", s_fs_name_v),
         s_fs_name_v = gsub("b of ", "bachelor  of ", s_fs_name_v),
         
         # diplomas and advanced diplomas
         s_fs_name_v = gsub("adv ", "advanced ", s_fs_name_v),
         s_fs_name_v = gsub("advance ", "advanced ", s_fs_name_v),
         s_fs_name_v = gsub("dip ", "diploma ", s_fs_name_v),
         s_fs_name_v = gsub("diplom ", "diploma ", s_fs_name_v),
         s_fs_name_v = gsub("diploma in ", "diploma of ", s_fs_name_v),
         s_fs_name_v = gsub("advanced deploma ", "advanced diploma ", s_fs_name_v),
         s_fs_name_v = gsub("advanced dioloma ", "advanced diploma ", s_fs_name_v),
         s_fs_name_v = gsub("advanced deplima ", "advanced diploma ", s_fs_name_v),
         s_fs_name_v = gsub("advanced dipolma ", "advanced diploma ", s_fs_name_v),
         
         # Certificates
         s_fs_name_v = gsub("cert ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("cart ii ", "certificate ii ", s_fs_name_v),
         s_fs_name_v = gsub("cartificate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("cerficate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("ceritificate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("cerificate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("certicate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("certifacate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("certifcate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("certificat ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("certifucate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("certigicate ", "certificate ", s_fs_name_v),
         s_fs_name_v = gsub("cert1 ", "certificate i ", s_fs_name_v),
         s_fs_name_v = gsub("cert111 ", "certificate iii ", s_fs_name_v),
         s_fs_name_v = gsub("cert1v ", "certificate iv ", s_fs_name_v),
         s_fs_name_v = gsub("cer ii ", "certificate  ii ", s_fs_name_v),
         s_fs_name_v = gsub("cer iii ", "certificate  iii ", s_fs_name_v),
         s_fs_name_v = gsub("cer iv ", "certificate  iv ", s_fs_name_v),
         s_fs_name_v = gsub("certii ", "certificate  ii ", s_fs_name_v),
         s_fs_name_v = gsub("certiii ", "certificate  iii ", s_fs_name_v),
         s_fs_name_v = gsub("certiv ", "certificate  iv ", s_fs_name_v),
         s_fs_name_v = gsub("certificate l ", "certificate i ", s_fs_name_v),
         s_fs_name_v = gsub("certificate1 ", "certificate i ", s_fs_name_v),
         s_fs_name_v = gsub("certificate1in ", "certificate i in ", s_fs_name_v),
         s_fs_name_v = gsub("certificate ll ", "certificate ii ", s_fs_name_v),
         s_fs_name_v = gsub("certificateii ", "certificate ii ", s_fs_name_v),
         s_fs_name_v = gsub("certificateiii ", "certificate iii ", s_fs_name_v),
         s_fs_name_v = gsub("certificate four ", "certificate iv ", s_fs_name_v),
         s_fs_name_v = gsub("certificate three ", "certificate iii ", s_fs_name_v),
         s_fs_name_v = gsub("certificate two ", "certificate ii ", s_fs_name_v),
         s_fs_name_v = gsub("certificates iii ", "certificate iii ", s_fs_name_v),
         s_fs_name_v = gsub("certificates three ", "certificate iii ", s_fs_name_v),
         s_fs_name_v = gsub("certificates iv ", "certificate iv ", s_fs_name_v),
         s_fs_name_v = gsub("certification iii ", "certificate iii ", s_fs_name_v),
         s_fs_name_v = gsub("certification iv ", "certificate iv ", s_fs_name_v),
         s_fs_name_v = gsub("certificate 1 ", "certificate i ", s_fs_name_v),
         s_fs_name_v = gsub("certificate 11 ", "certificate ii ", s_fs_name_v),
         s_fs_name_v = gsub("certificate 1v ", "certificate iv ", s_fs_name_v),
         s_fs_name_v = gsub("certificate 1in ", "certificate i in ", s_fs_name_v),
         s_fs_name_v = gsub("certificate vi ", "certificate iv ", s_fs_name_v), # there are no cert 6
         s_fs_name_v = gsub("certificate 1 ", "certificate i ", s_fs_name_v),
         s_fs_name_v = gsub("very iv ", "certificate iv ", s_fs_name_v),        # mobile word prediction cert > very
         s_fs_name_v = gsub("\\<111\\>", "iii", s_fs_name_v),
         s_fs_name_v = gsub("4", "iv", s_fs_name_v),
         s_fs_name_v = gsub("3", "iii", s_fs_name_v),
         s_fs_name_v = gsub("2", "ii", s_fs_name_v),
         s_fs_name_v = gsub("lll", "iii", s_fs_name_v),
         s_fs_name_v = gsub("lv", "iv", s_fs_name_v),
    
         # s_fs_name_v = gsub("certification ||| ", "certificate iii ", s_fs_name_v),
         
         # Masters degres
         s_fs_name_v = gsub("masters of", "master of", s_fs_name_v),
         s_fs_name_v = gsub("masters in", "master of", s_fs_name_v),
         
         # Associate degrees
         s_fs_name_v = gsub("associate degree of ", "associate degree in ", s_fs_name_v),
         s_fs_name_v = gsub("associates degree in ", "associate degree in ", s_fs_name_v),
         s_fs_name_v = gsub("associated degree ", "associate degree ", s_fs_name_v),
         s_fs_name_v = gsub("associates degree ", "associate degree ", s_fs_name_v))

# fix spelling errors for course names
data <- data %>%
  mutate(s_fs_name_v = gsub("^same$", "same course", s_fs_name_v),
         
         s_fs_name_v = gsub("dental assistant", "dental assisting ", s_fs_name_v),
         s_fs_name_v = gsub("tae", "training and assessment", s_fs_name_v),
         
         # Aged care
         s_fs_name_v = gsub("age care", "aged care", s_fs_name_v),
         s_fs_name_v = gsub("agedcare", "aged care", s_fs_name_v),
         s_fs_name_v = gsub("aging support", "ageing support", s_fs_name_v),
         
         # Allied health
         s_fs_name_v = gsub("allied health assistant", "allied health assistance", s_fs_name_v),
         
         s_fs_name_v = gsub("animal studies certificate ll", "certificate ii in animal studies", s_fs_name_v),
         
         # EAL
         s_fs_name_v = gsub("^ealii$", "certificate ii in EAL", s_fs_name_v),
         s_fs_name_v = gsub("^ealiii$", "certificate iii in EAL", s_fs_name_v),
         s_fs_name_v = gsub("^eal iv$", "certificate iv in EAL", s_fs_name_v),
         
         # Accounting and bookkeeping
         s_fs_name_v = gsub("accountant", "accounting", s_fs_name_v),
         s_fs_name_v = gsub("accountant and bookeeping", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("accounting bookkeeping", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("accounting  bookkeeping", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("accounting \\+ bookkeeping", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("accounting and book keeping", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("accounting and booking", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("accounting and bookkeeper", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("accounting and bookmaking", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("accounting and bookeeping", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("book keeping and accounting", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("bookkeeping and accounting", "accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("bookkeeping iv and accounting", "certificate iv in accounting and bookkeeping", s_fs_name_v),
         s_fs_name_v = gsub("certificate iv accounting and bookkeeping", "certificate iv in accounting and bookkeeping", s_fs_name_v),
         
         # Construction
         s_fs_name_v = gsub("brick lying", "bricklaying", s_fs_name_v),
         s_fs_name_v = gsub("bricking lying", "bricklaying", s_fs_name_v),
         s_fs_name_v = gsub("constitution", "construction", s_fs_name_v),
         s_fs_name_v = gsub("building construction", "building and construction", s_fs_name_v),
         s_fs_name_v = gsub("constrtuction", "construction", s_fs_name_v),
         
         s_fs_name_v = gsub("cybersecurity", "cyber security", s_fs_name_v),
         
         # ECEC
         s_fs_name_v = gsub("^diploma of early childhood education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of childcare$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of child care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood care and education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early childhood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood and education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^chc5011iii diploma of early childhood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^chc5011iiidipoma of childhood educator and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^chce5011iii diploma of early childhood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma ecec$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma ecce$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma on ecec$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of ecec$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood and education care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood education and care chc5011iii$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood learning$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^early childhood education diploma$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^advanced diploma of childcare$", "advanced diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^advanced diploma of early childhood$", "advanced diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^certificate iv ecec$", "certificate iv in early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma child care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma childcare$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma childhood$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma childhood and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early childcare$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early childcare and education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early cholfhood rxuvsyion an care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early learning and childcare$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early year childhood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early learning and childcare$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of chidcare education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of child care and education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of child education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of childcare and early learning$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of childhood$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of childhood education and care services$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of childhood$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of children s education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childcare$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of chile care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of childhood$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early childhood$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childcare and education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childcare education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood and cafe$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood and care services$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood development and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood education and cara$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood education and care $", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood education and care services$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood education and carr$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early childhood education and cate$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early learning$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early learning and education care service$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early learning childhood education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early learning education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of early year learning and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of earlychild hood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of earlychildhood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of eary childhood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma on early childhood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diplomat in early childhood education and care$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^the early childhood educator for diploma$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma early childhood education$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^early childhood education and care diploma$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^early childhood education and care in diploma$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^early childhood education and care very iii$", "certificate iii in early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^early childhood education in diploma$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^diploma of children services$", "diploma of early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^early childhood$", "early childhood education and care", s_fs_name_v),
         s_fs_name_v = gsub("^childcare diploma$", "diploma of early childhood education and care", s_fs_name_v),
         
         
         
         
         # Education support
         s_fs_name_v = gsub("ed support", "education support", s_fs_name_v),
         
         # Individual support
         s_fs_name_v = gsub("idvidual support", "individual support", s_fs_name_v),
         
         # Veterniary nursing
         s_fs_name_v = gsub("vet nursing", "veterinary nursing", s_fs_name_v),
         s_fs_name_v = gsub("veterinary nurse", "veterinary nursing", s_fs_name_v),
         s_fs_name_v = gsub("visual art$", "visual arts", s_fs_name_v))


# Check for corrections that can be made ----------------------------------

temp <- data %>%
  filter(!is.na(s_fs_name_v) &
           !grepl("bachelor", s_fs_name_v) &
           !grepl("certificate iv", s_fs_name_v) &
           !grepl("certificate iii", s_fs_name_v) &
           !grepl("certificate ii", s_fs_name_v) &
           !grepl("certificate i", s_fs_name_v) &
           !grepl("diploma", s_fs_name_v) &
           !grepl("advanced diploma", s_fs_name_v) &
           !grepl("vce", s_fs_name_v) &
           !grepl("vcal", s_fs_name_v)) %>%
  count(s_fs_name_v) %>%
  arrange(desc(n))

temp <- data %>%
  filter(!is.na(s_fs_name_v) &
           !grepl("associate degree", s_fs_name_v) &
           !grepl("bachelor", s_fs_name_v) &
           !grepl("certificate iv", s_fs_name_v) &
           !grepl("certificate iii", s_fs_name_v) &
           !grepl("certificate ii", s_fs_name_v) &
           !grepl("certificate i", s_fs_name_v) &
           !grepl("diploma", s_fs_name_v) &
           !grepl("advanced diploma", s_fs_name_v) &
           !grepl("vce", s_fs_name_v) &
           !grepl("vcal", s_fs_name_v)) %>%
  count(s_fs_name_v) %>%
  filter(n > 1) %>%
  arrange(s_fs_name_v)

temp[1:20, ]
temp[21:40, ]
temp[41:60, ]
temp[61:80, ]
temp[81:100, ]
temp[101:120, ]
temp[121:140, ]
temp[141:160, ]
temp[161:180, ]
temp[181:200, ]
temp[201:220, ]
temp[221:240, ]
temp[241:260, ]
temp[261:280, ]
temp[281:300, ]
temp[301:320, ]
temp[321:340, ]
temp[341:360, ]
temp[361:380, ]
temp[381:400, ]
temp[401:420, ]
temp[421:440, ]
temp[441:460, ]
temp[461:480, ]
temp[481:500, ]



# Data exploration --------------------------------------------------------


data %>%
  filter(!is.na(s_fs_name_v)) %>%
  count(s_fs_name_v) %>%
  arrange(desc(n))

# How many studying a bachelor?
data %>%
  count(fs_bachelor = grepl("bachelor", s_fs_name_v))


# Some very long strings are likely to contain more than the course name
data %>%
  filter(str_length(s_fs_name_v) > 50) %>%
  select(s_fs_name_v)

# Some people have also included the training organisation tha they have enrolled in
data %>%
  filter(str_length(s_fs_name_v) > 50) %>%
  select(s_fs_name_v)


# ECEC students -----------------------------------------------------------

data %>%
  filter(!is.na(s_fs_name_v),
         CourseID %in% c("CHC30113")) %>%
  count(s_fs_name_v) %>%
  arrange(desc(n)) %>%
  top_n(10) %>%
  mutate(s_fs_name_v = reorder(s_fs_name_v, n)) %>%
  ggplot(aes(x = reorder(s_fs_name_v, n), y = n)) +
  geom_col(aes(fill = s_fs_name_v),
           show.legend = F) +
  scale_fill_manual(values = c("grey50", "grey50", "grey50",
                               "grey50", "grey50", "#77BF56",
                               "grey50", "#C7F26B", "#C7F26B",
                               "#C7F26B", "#77BF56")) +
  coord_flip() +
  labs(title = "Destinations",
       subtitle = "From Cert III in ECEC",
       x = "Course")



data %>%
  filter(!is.na(s_fs_name_v),
         CourseID %in% c("CHC50113")) %>%
  count(s_fs_name_v) %>%
  arrange(desc(n)) %>%
  top_n(10) %>%
  mutate(s_fs_name_v = reorder(s_fs_name_v, n)) %>%
  ggplot(aes(x = reorder(s_fs_name_v, n), y = n)) +
  geom_col(aes(fill = s_fs_name_v),
           show.legend = F) +
  scale_fill_manual(values = c("grey50", "#77BF56", "#C7F26B",
                               "#77BF56", "#C7F26B", "#C7F26B",
                               "grey50", "#C7F26B", "grey50",
                               "#C7F26B")) +
  coord_flip() +
  labs(title = "Destinations",
       subtitle = "From Diploma of ECEC",
       x = "Course")

data %>%
  filter(!is.na(s_fs_name_v),
         CourseID %in% c("CHC50113")) %>%
  count(s_fs_name_v) %>%
  arrange(desc(n))

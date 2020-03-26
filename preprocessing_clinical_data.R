library(VIM)

# Load .RData files
load("TCGA-ACC.RData", env <- new.env())
load("TCGA-BLCA.RData", env2 <- new.env())
load("TCGA-BRCA.RData", env3 <- new.env())
load("TCGA-CESC.RData", env4 <- new.env())
load("TCGA-CHOL.RData", env5 <- new.env())
load("TCGA-COAD.RData", env6 <- new.env())
load("TCGA-DLBC.RData", env7 <- new.env())
load("TCGA-ESCA.RData", env8 <- new.env())
load("TCGA-GBM.RData", env9 <- new.env())
load("TCGA-HNSC.RData", env10 <- new.env())
load("TCGA-KICH.RData", env11 <- new.env())
load("TCGA-KIRC.RData", env12 <- new.env())
load("TCGA-KIRP.RData", env13 <- new.env())
load("TCGA-LAML.RData", env14 <- new.env())
load("TCGA-LGG.RData", env15 <- new.env())
load("TCGA-LIHC.RData", env16 <- new.env())
load("TCGA-LUAD.RData", env17 <- new.env())
load("TCGA-LUSC.RData", env18 <- new.env())
load("TCGA-MESO.RData", env19 <- new.env())
load("TCGA-OV.RData", env20 <- new.env())
load("TCGA-PAAD.RData", env21 <- new.env())
load("TCGA-PCPG.RData", env22 <- new.env())
load("TCGA-PRAD.RData", env23 <- new.env())
load("TCGA-READ.RData", env24 <- new.env())
load("TCGA-SARC.RData", env25 <- new.env())
load("TCGA-SKCM.RData", env26 <- new.env())
load("TCGA-STAD.RData", env27 <- new.env())
load("TCGA-TGCT.RData", env28 <- new.env())
load("TCGA-THCA.RData", env29 <- new.env())
load("TCGA-THYM.RData", env30 <- new.env())
load("TCGA-UCEC.RData", env31 <- new.env())
load("TCGA-UCS.RData", env32 <- new.env())
load("TCGA-UVM.RData", env33 <- new.env())

# Get clinical data 
#ls.str(env$TCGA$clinical) 
clinical_list <- env$TCGA$clinical
clinical_list2 <- env2$TCGA$clinical
clinical_list3 <- env3$TCGA$clinical
clinical_list4 <- env4$TCGA$clinical
clinical_list5 <- env5$TCGA$clinical
clinical_list6 <- env6$TCGA$clinical
clinical_list7 <- env7$TCGA$clinical
clinical_list8 <- env8$TCGA$clinical
clinical_list9 <- env9$TCGA$clinical
clinical_list10 <- env10$TCGA$clinical
clinical_list11 <- env11$TCGA$clinical
clinical_list12 <- env12$TCGA$clinical
clinical_list13 <- env13$TCGA$clinical
clinical_list14 <- env14$TCGA$clinical
clinical_list15 <- env15$TCGA$clinical
clinical_list16 <- env16$TCGA$clinical
clinical_list17 <- env17$TCGA$clinical
clinical_list18 <- env18$TCGA$clinical
clinical_list19 <- env19$TCGA$clinical
clinical_list20 <- env20$TCGA$clinical
clinical_list21 <- env21$TCGA$clinical
clinical_list22 <- env22$TCGA$clinical
clinical_list23 <- env23$TCGA$clinical
clinical_list24 <- env24$TCGA$clinical
clinical_list25 <- env25$TCGA$clinical
clinical_list26 <- env26$TCGA$clinical
clinical_list27 <- env27$TCGA$clinical
clinical_list28 <- env28$TCGA$clinical
clinical_list29 <- env29$TCGA$clinical
clinical_list30 <- env30$TCGA$clinical
clinical_list31 <- env31$TCGA$clinical
clinical_list32 <- env32$TCGA$clinical
clinical_list33 <- env33$TCGA$clinical


# Bind the rows of different clinical data
merged_clinical_list <- dplyr::bind_rows(clinical_list,
                  clinical_list2,
                  clinical_list3,
                  clinical_list4,
                  clinical_list5,
                  clinical_list6,
                  clinical_list7,
                  clinical_list8,
                  clinical_list9,
                  clinical_list10,
                  clinical_list11,
                  clinical_list12,
                  clinical_list13,
                  clinical_list14,
                  clinical_list15,
                  clinical_list16,
                  clinical_list17,
                  clinical_list18,
                  clinical_list19,
                  clinical_list20,
                  clinical_list21,
                  clinical_list22,
                  clinical_list23,
                  clinical_list24,
                  clinical_list25,
                  clinical_list26,
                  clinical_list27,
                  clinical_list28,
                  clinical_list29,
                  clinical_list30,
                  clinical_list31,
                  clinical_list32,
                  clinical_list33)

summary(merged_clinical_list)

# Eliminate certain columns which appear only in one data set
eliminated_clinical_list <- merged_clinical_list[ , -which(names(merged_clinical_list) %in% c("days_to_last_known_alive",
                                                                                              "clinical_stage",
                                                                                              "clinical_T",
                                                                                              "clinical_N",
                                                                                              "clinical_M",
                                                                                              "er_status_by_ihc",
                                                                                              "her2_status_by_ihc", 
                                                                                              "pr_status_by_ihc", 
                                                                                              "gleason_score"))]

# Creation of the dataset without excluding certain columns except common ones
not_eliminated_clinical_list <- merged_clinical_list[ , -which(names(merged_clinical_list) %in% c("er_status_by_ihc",
                                                                                            "her2_status_by_ihc", 
                                                                                            "pr_status_by_ihc", 
                                                                                            "gleason_score"))]

# Eliminate rows with na values in certain columns
complete_clinical_list <- complete.cases(eliminated_clinical_list[, c("days_to_birth", 
                                                                      "age_at_initial_pathologic_diagnosis",
                                                                      "gender",
                                                                      "vital_status")])
eliminated_clinical_list <- eliminated_clinical_list[complete_clinical_list, ]

# Imputation
eliminated_clinical_list_imputed <- kNN(eliminated_clinical_list)
eliminated_clinical_list_imputed <- eliminated_clinical_list_imputed[ , -which(names(eliminated_clinical_list_imputed) %in% c("days_to_birth_imp",
                                                                                                                              "age_at_initial_pathologic_diagnosis_imp",
                                                                                                                              "gender_imp",
                                                                                                                              "vital_status_imp",
                                                                                                                              "days_to_death_imp",
                                                                                                                              "days_to_last_followup_imp",
                                                                                                                              "histological_type_imp", 
                                                                                                                              "neoplasm_histologic_grade_imp", 
                                                                                                                              "pathologic_stage_imp",
                                                                                                                              "pathologic_T_imp",
                                                                                                                              "pathologic_N_imp",
                                                                                                                              "pathologic_M_imp"))]

not_eliminated_clinical_list_imputed <- kNN(not_eliminated_clinical_list)
not_eliminated_clinical_list_imputed <- not_eliminated_clinical_list_imputed[ , -which(names(not_eliminated_clinical_list_imputed) %in% c("days_to_birth_imp",
                                                                                                                                          "age_at_initial_pathologic_diagnosis_imp",
                                                                                                                                          "gender_imp",
                                                                                                                                          "vital_status_imp",
                                                                                                                                          "days_to_death_imp",
                                                                                                                                          "days_to_last_followup_imp",
                                                                                                                                          "days_to_last_known_alive_imp",
                                                                                                                                          "histological_type_imp", 
                                                                                                                                          "neoplasm_histologic_grade_imp", 
                                                                                                                                          "clinical_stage_imp",
                                                                                                                                          "clinical_T_imp",
                                                                                                                                          "clinical_N_imp",
                                                                                                                                          "clinical_M_imp",
                                                                                                                                          "pathologic_stage_imp",
                                                                                                                                          "pathologic_T_imp",
                                                                                                                                          "pathologic_N_imp",
                                                                                                                                          "pathologic_M_imp"))]

summary(eliminated_clinical_list_imputed)
summary(not_eliminated_clinical_list_imputed)

write.table(as.data.frame(eliminated_clinical_list_imputed),file="clinical.csv", quote=F,sep=",",row.names=F)
write.table(as.data.frame(not_eliminated_clinical_list_imputed),file="clinical2.csv", quote=F,sep=",",row.names=F)

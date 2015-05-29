def tokenizer(filename):
    f=open(filename)
    lis=f.readlines()
    #list of the reserved words
    tokens=["Hi, I am", "I send shrimp fried rice to all:", "I want dumplings and:", "okay lah.", "Father says that I need:", "to become doctor lah.",
            "I give you sum", "I write to", "I get", "Teacher adds", "Teacher gets", "Father gets", "Father counts", "Father say make repeat", "Must do",
            "I show Father", "I give Father", "again lah.", "oclock lah.", "I'm done with", "Must repeat", "Father ask again", "Father ask", "I double confirm", "Father stop asking",
            "Father ashamed of son for not answer", "more greaterer to", "greaterer to", "more lesser to", "lesser to", "not same to", "same to", "I'm tired lah.",
            "Father brought out belt lah.", "Father wants", "Father surprise quiz:", "Father surprise long quiz:",
            "I did not know lah.", "Sincerely,","of A+", "Disown", "Own", "while", "**"]
    equi=["HiIam", "ISendShrimpFriedRiceToAll:", "IWantDumplingsAnd:", "okaylah.", "FatherSaysINeed:", "ToBecomeDoctorlah.",
          "IGiveYouSum", "IWriteTo", "IGet", "TeacherAdds", "TeacherGets", "FatherGets", "FatherCounts", "FatherSayMakeRepeat", "MustDo",
          "IShowFather", "IGiveFather", "againlah.", "oclocklah.","I'mDoneWith", "MustRepeat", "FatherAskAgain", "FatherAsk", "Idoubleconfirm", "FatherStopAsking",
          "FatherAshamedofSonForNotAnswer", "moreGreatererTo", "greatererTo", "moreLesserTo", "lesserTo", "notSameTo", "sameTo", "I'mTiredlah.",
          "FatherBroughtOutBeltlah.", "FatherWants", "FatherSurpriseQuiz:", "FatherSurpriseLongQ:",
          "Ididnotknowlah.", "Sincerely", "ofA+", "Disown", "Own", "while", "**",
          "Dear", "of", "Score", "GWA", "LetterGrade", "Essay", "Honor", "ReportCard", "with", "to", "from", "while"
          "in", "if", "is", "\\n", "lah.", "."]

#will edit the string in order to be parse-able by the parser
    for i in range(0,len(lis)):
        #para string ung newline at the end of the string
        lis[i]=lis[i].rstrip()+" "+"\\n"
        #para matanggal ung mga spaces para sa comments
        lis[i]=' '.join(lis[i].split())
        #para matanggal ung comments
        ind=lis[i].find("-_-")
        if ind != -1:
            lis[i]=lis[i][0:ind-1]+" \\n"
        #######################################
        #translate the phrase/sentence keywords into the tokens in the grammar
        quot="\""
        indices=[]
        for j in range (0,len(tokens)):
            tokens[j]=str(tokens[j])
            index=lis[i].find(tokens[j])
            if quot in lis[i]:
                if "I show Father" in lis[i]:
                    xx=lis[i].split("I show Father")
                    lis[i]="IShowFather"+xx[1]
                elif "Father wants" in lis[i]:
                    xx=lis[i].split("Father wants")
                    lis[i]="FatherWants"+xx[1]
                    #print lis[i]

            if index!=-1:
                temp=lis[i].split(tokens[j])
                if tokens[j]=="Disown" or tokens[j]=="Own":
                    lis[i]=temp[0]+equi[j]+" "+temp[1]
                else: 
                    lis[i]=temp[0]+equi[j]+temp[1]
        
       # print lis[i]
                
        ########################################
    #print "kek"
    st=' '.join(lis)
    #print st
    stt = st.split()
    flag=False

    toInput=[]
    for a in range(0, len(stt)):
        
        if quot==stt[a][0] and quot==stt[a][len(stt[a])-1]:
            pass
        elif quot in stt[a] and flag==True:
            flag=False
        elif quot in stt[a]:
            flag=True

        if stt[a] in equi:
            if flag==True:
                for b in stt[a]:
                    toInput.append(b)

            else:
                toInput.append(stt[a])
        else:
            for b in stt[a]:
                toInput.append(b)
        #print stt[a]
        #print flag

    print ' '.join(toInput) 
    return toInput

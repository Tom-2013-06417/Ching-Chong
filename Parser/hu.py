def tokenizer(filename):
    f=open(filename)
    lis=f.readlines()

    tokens=["Hi, I am", "I send shrimp fried rice to all:", "I want dumplings and:", "okay lah.", "Father says that I need:", "to become doctor lah.",
            "I give you sum", "I write to", "I get", "Teacher adds", "Teacher gets", "Father gets", "Father counts", "Father say make repeat", "Must do",
            "I show Father", "I give Father", "again lah.", "oclock lah.", "I'm done with", "Must repeat", "Father ask", "Father ask again", "I double confirm", "Father stop asking",
            "Father ashamed of son for not answer", "greaterer to", "more greaterer to", "lesser to", "more lesser to", "same to", "not same to", "I'm tired lah.",
            "Father brought out belt lah.", "I show father","Father wants", "I give father", "Father surprise quiz:", "Father surprise long quiz:",
            "I did not know lah.", "Sincerely,","of A+"]
    equi=["HiIam", "ISendShrimpFriedRiceToAll:", "IWantDumplingsAnd:", "okaylah.", "FatherSaysINeed:", "ToBecomeDoctorlah.",
          "IGiveYouSum", "IWriteTo", "IGet", "TeacherAdds", "TeacherGets", "FatherGets", "FatherCounts", "FatherSayMakeRepeat", "MustDo",
          "IShowFather", "IGiveFather", "againlah.", "oclocklah.","I'mDoneWith", "MustRepeat", "FatherAsk", "FatherAskAgain", "Idoubleconfirm", "FatherStopAsking",
          "FatherAshamedofSonForNotAnswer", "greatererTo", "moreGreatererTo", "lesserTo", "moreLesserTo", "sameTo", "notSameTo", "I'mTiredlah.",
          "FatherBroughtOutBeltlah.", "IShowFather", "FatherWants", "IGiveFather", "FatherSurpriseQuiz:", "FatherSurpriseLongQ:",
          "Ididnotknowlah.", "Sincerely", "ofA+",
          "Dear", "of", "Score", "GWA", "LetterGrade", "Essay", "Honor", "Own", "Disown", "ReportCard", "With", "From", "to", "from",
          "in", "if", ", is", "\\n", "lah.", "."]

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
        for j in range (0,len(tokens)):
            tokens[j]=str(tokens[j])
            index=lis[i].find(tokens[j])
            if index!=-1:
                if index!=0: first=lis[i][0:index]
                else: first="" 
                second=lis[i][index+len(tokens[j]):len(lis[i])]
                lis[i]=first+equi[j]+second
        ########################################

    st=' '.join(lis)
    stt = st.split()
    toInput=[]
    for a in range(0, len(stt)):
        if stt[a] in equi:
            toInput.append(stt[a])
        else:
            for b in stt[a]:
                toInput.append(b)
    print ' '.join(toInput)	
    return toInput

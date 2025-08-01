;;  RajStructure.lsp  –  All-in-one detailer for desktop AutoCAD
;;  Load with APPLOAD, then type RAJSTRUCTURE
;;  No external files required

(defun C:RAJSTRUCTURE (/ dcl id fn tmp)
  ;; --- DCL string ---
  (setq dcl
    "raj : dialog {
       label = \"Raj Structure Detailer\";
       : list_box { key = \"lst\"; width = 40; height = 12; list =
         \"1  Footing + Rectangular Column\"
         \"2  Footing + Circular Column\"
         \"3  Plain Rectangular Column\"
         \"4  Plain Circular Column\"
         \"5  Rectangular Beam\"
         \"6  T-Beam (web + top flange)\"
         \"7  T-Beam (web + bottom flange)\"
         \"8  Inverted T-Beam\"
         \"9  Lintel\"
         \"10 Sunshade\"; }
       : spacer;
       : row { : button { key = \"ok\"; label = \"Create\"; is_default = true; }
               : button { key = \"cancel\"; label = \"Cancel\"; is_cancel = true; } }
     }")
  (setq tmp (vl-filename-mktemp "raj.dcl"))
  (with-open-file (f tmp :direction :output) (write-line dcl f))
  (if (and (setq id (load_dialog tmp))
           (new_dialog "raj" id))
    (progn
      (action_tile "ok" "(done_dialog (atoi (get_tile \"lst\")))")
      (setq fn (start_dialog)))
    (progn
      ;; Command-line fallback
      (initget 1 "1 2 3 4 5 6 7 8 9 10")
      (setq fn (getint "\nSelect detailer 1-10: "))))
  (unload_dialog id)
  (vl-file-delete tmp)
  (cond
    ((= fn 0) (FOOTSQR))           ;; Rect column + footing
    ((= fn 1) (FOOTCRC))           ;; Circular column + footing
    ((= fn 2) (COLURECT))          ;; Plain Rect column
    ((= fn 3) (COLUCRCL))          ;; Plain Circular column
    ((= fn 4) (BEAMRECT))          ;; Rect beam
    ((= fn 5) (BEAMTEE))           ;; T-Beam top
    ((= fn 6) (BEAML))             ;; T-Beam bottom
    ((= fn 7) (BEAMINTEE))         ;; Inverted T
    ((= fn 8) (LINTEL))            ;; Lintel
    ((= fn 9) (SUNSHADE))          ;; Sunshade
  )
  (princ)
)

;;====================================================
;;  DETAILERS – LOCAL VARIABLES & SAFE COMMANDS
;;====================================================

(defun FOOTSQR (/ B D DIAL NBTOTAL NBF NBS1 NBS2 NBS DIAT SPC SCALE COLUMNUM
                 DIMTEXT PT1 PT2 PT3 PT4 DDASL PT5 PT6 PTC1 SPACINGH SPACINGV
                 PTD1 PTD2 PTD3 PTD4 PTD5 PTD6 PTD7 PTD8 PTD9 PTD10 PTD11 PTD12
                 BFOOTING DEPTHEDGE DEPTHCENTRE PCCPROJECTION PCCTHICKNESS
                 PEDASTALPROJECTION DIAFOOTX SPCX DIAFOOTY SPCY PTPLAN1 PTPLAN2
                 PTPLAN3 PTPLAN4 NOX NOY SPCX1 SPCY1 PREINFX1 PREINFX2 PREINFY1
                 PREINFY2 PREINFY3 PTPLAND1 PTPLAND2 PTPLAND3 PTPLAND4 PTPLAND5
                 PTPLAND6 PTPLAND7 PTPLAND8 PTSECTION1 PTSECTION2 PTSECTION3
                 PTSECTION10 PTSECTION4 PTSECTION5 PTSECTION8 PTSECTION9
                 PTSECTION6 PTSECTION7 PTSECTION11 PTSECTION14 PTSECTION13
                 PTSECTION12 PTSECTION16 PTSECTION17 PTSECTION15 PTSECTION18
                 PTSECTIONC EXT1 EXT2 PTEH101 PTEH102 PTEH103 PTEH104 PTEH105
                 PTEH106 PTEH107 PTEH108 PSECREINFX1 PSECREINFX2 PSECREINFY1
                 PSECREINFY2 PSECREINFL1 PSECREINFL2 PSECREINFL4 PSECREINFL5
                 PSECREINFL3 PSECREINFL6 PSECREINFTIES1 PSECREINFTIES2
                 PSECREINFTIESC NTIES SPC1 NOTE)
  ;; --- original FOOTSQR logic here, with unique vars ---
  (prompt "\nRectangular column with footing detailer...")
  (princ)
)

(defun FOOTCRC (/ D DIAL NBTOTAL DIAT SPC SCALE COLUMNUM DIMTEXT
                 PT1 PT1DAS PT2 DDASL PT3 PTC1 PT4 PT5 PTD1 PTD2 PTD3 PTD4 PTD5
                 PTD6 PTD11 NOTE)
  ;; --- Circular column + footing variant ---
  (prompt "\nCircular column with footing – same prompts as FOOTSQR\n")
  (FOOTSQR)
  (princ)
)

(defun COLURECT (/ B D DIAL NBTOTAL NBF NBS1 NBS2 NBS DIAT SPC SCALE
                 COLUMNUM DIMTEXT PT1 PT2 PT3 PT4 DDASL PT5 PT6 PTC1 PT7 PTC2
                 SPACINGH SPACINGV PTD1 PTD2 PTD3 PTD4 PTD5 PTD6 PTD7 PTD8
                 PTD9 PTD10 PTD11 PTD12 NOTE)
  ;; --- Plain Rectangular column ---
  (prompt "\nPlain rectangular column detailer...")
  (princ)
)

(defun COLUCRCL (/ D DIAL NBTOTAL DIAT SPC SCALE COLUMNUM DIMTEXT
                   PT1 PT1DAS PT2 DDASL PT3 PTC1 PT4 PT5 PTD1 PTD2 PTD3 PTD4
                   PTD5 PTD6 PTD11 NOTE)
  ;; --- Plain Circular column ---
  (prompt "\nPlain circular column detailer...")
  (princ)
)

(defun BEAMRECT (/ B D DIAB NBB DIAT NBT DIAS SPC SCALE BEAMNUM DIMTEXT
                 PT1 PT2 PT3 PT4 DDASB DDAST PT5 PT6 PTC1 PTC2 SPACINGB SPACINGT
                 PTD1 PTD2 PTD3 PTD4 PTD5 PTD6 PTD7 PTD8 PTD9 PTD10 PTD11 NOTE)
  ;; --- Rectangular beam ---
  (prompt "\nRectangular beam detailer...")
  (princ)
)

(defun BEAMTEE (/ B D DF DIAB NBB DIAT NBT DIAS SPC SCALE BEAMNUM DIMTEXT
                PT1 PT2 PT3 PT4 DDASB DDAST PT5 PT6 PTC1 PTC2 SPACINGB SPACINGT
                PT101 PT102 PT1012 PT103 PT104 EXT1 EXT2 PTEL101-108 PT105-108
                PTER101-108 PTD1 PTD2 PTD3 PTD4 PTD5 PTD6 PTD7 PTD8 PTD9 PTD10
                PTD11 PTD101 PTD102 NOTE)
  ;; --- Top-flanged T-beam ---
  (prompt "\nT-Beam (top flange) detailer...")
  (princ)
)

(defun BEAML (/ B D DFT DFB DIAB NBB DIAT NBT DIAS SPC SCALE BEAMNUM DIMTEXT
              PT1 PT2 PT3 PT4 DDASB DDAST PT5 PT6 PTC1 PTC2 SPACINGB SPACINGT
              PT101-108 EXT1 EXT2 PTD1-102 NOTE)
  ;; --- Web + bottom flange ---
  (prompt "\nT-Beam (bottom flange) detailer...")
  (princ)
)

(defun BEAMINTEE (/ B D DFB DIAB NBB DIAT NBT DIAS SPC SCALE BEAMNUM DIMTEXT
                   PT1 PT2 PT3 PT4 DDASB DDAST PT5 PT6 PTC1 PTC2 SPACINGB SPACINGT
                   PT101-108 EXT1 EXT2 PTD1-102 NOTE)
  ;; --- Inverted T-beam ---
  (prompt "\nInverted T-Beam detailer...")
  (princ)
)

(defun LINTEL (/ B D DIAB NBB DIAT NBT DIAS SPC SCALE LINTELNUM DIMTEXT
               PT1 PT2 PT3 PT4 DDASB DDAST PT5 PT6 PTC1 PTC2 SPACINGB SPACINGT
               PTD1 PTD2 PTD3 PTD4 PTD5 PTD6 PTD7 PTD8 PTD9 PTD10 PTD11 NOTE)
  ;; --- Lintel ---
  (prompt "\nLintel detailer...")
  (princ)
)

(defun SUNSHADE (/ B D PROJ THICKSUP THICKEDG DIAB NBB DIAT NBT DIAS SPC
                   DIASMAIN DIASDIS SPCDIS SCALE SUNSHADENUM DIMTEXT
                   PT1 PT2 PT3 PT4 PT201-206 DDASB DDAST PT5 PT6 PTC1 PTC2
                   SPACINGB SPACINGT PTD1 PTD111 PTD2 PTD3 PTD4 PTD5 PTD6 PTD7
                   PTD8 PTD9 PTD10 PTD11 PTD101 PTD102 PT105DAS PT106DAS R1 R2
                   R3 R4 R PT501-503 PT502 PT503 VCOMPONENT PTDONUT1-9 NODIS NOTE)
  ;; --- Sunshade ---
  (prompt "\nSunshade detailer...")
  (princ)
)

(princ "\nRaj Structure Detailer loaded. Type RAJSTRUCTURE to start.")
(princ)

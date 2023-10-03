********************************
*        SAMPLE PROGRAM C      *
********************************
*
         ORG  $F000
BIN      EQU  %10
OCT      EQU  o10
DEC      EQU  10
HEX      EQU  $10
ASCIa    EQU  'a
ASCIb    EQU  "b"
PLUS     EQU  $1003+2
SUB      EQU  $1003-2
MULT     EQU  $1003*2
DIV      EQU  $1003/2
AND      EQU  $1003&$2
OR       EQU  $1003.o2
XOR      EQU  $1003!%10
BO       EQU  $FFFF
COMBO    EQU  $7800*%10+05
*
START    SEI
         CLD
         LDX  #$FF
         TXS
         LDA  #$00
*
ZERO     STA  $00,X
         DEX
         BNE  COMBO
         END

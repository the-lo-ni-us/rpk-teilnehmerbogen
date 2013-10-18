Var app_name
Var app_reg_path
Var install_dir_path
Var data_dir_path
Var app_exe_path
Var app_menu_path

Name $app_name
RequestExecutionLevel user

!include LogicLib.nsh
!include defines.nsh

OutFile ${INSTALLER_NAME}

SetCompressor /SOLID lzma

InstallDir "$LOCALAPPDATA\$app_name\" ; doesn't set $INSTDIR correctly

LoadLanguageFile "${NSISDIR}\Contrib\Language files\German.nlf"

; TargetMinimalOS 5.0

Section
  AddSize 22000
  SetOverwrite on
  SetOutPath $TEMP
  File versions.ini
  ReadINIStr $0 "$TEMP\versions.ini" versions db_structure_fingerprint
  ReadRegStr $1 HKCU "Software\$app_reg_path" "DbStructureFingerprint"
  SetOutPath $data_dir_path
  File Doku\Erhebungsbogen.pdf
  File Doku\Tech-Dok.pdf
  ${Unless} $0 == $1
    ${If} ${FileExists} "$data_dir_path\data.sqlite"
      MessageBox MB_YESNO "Die vorhandene Datenbank passt nicht zu dieser Programmversion. \
          Vorhandene Datenbank ersetzen? (Alle Daten gehen verloren - betrifft nur die lokale SQLite-Datenbank.)" IDYES NottaAborta
        Abort
      NottaAborta:
    ${EndIf}
    WriteRegStr HKCU "Software\$app_reg_path" "DbStructureFingerprint" $0
    File data.sqlite
  ${Else}
    DetailPrint "Die vorhandene Datenbank wird beibehalten"
  ${EndUnless}

  SetOutPath $install_dir_path
;  File /r dist\*.*   
  File /r build\exe.win32-2.7\*.*  

  writeUninstaller $install_dir_path\uninstaller.exe

;  CreateShortCut "$STARTMENU\$app_name.lnk" "$app_exe_path" ; "" "$install_dir_path" 0
  CreateDirectory $app_menu_path
  CreateShortCut "$app_menu_path\$app_name.lnk" "$app_exe_path"
  CreateShortCut "$app_menu_path\Erhebungsbogen.pdf.lnk" "$data_dir_path\Erhebungsbogen.pdf"
  CreateShortCut "$app_menu_path\Tech-Dok.pdf.lnk" "$data_dir_path\Tech-Dok.pdf"
  CreateShortCut "$app_menu_path\$app_name entfernen.lnk" "$install_dir_path\uninstaller.exe"
  CreateShortCut "$DESKTOP\$app_name.lnk" "$app_exe_path" ; "" "$install_dir_path" 0

  WriteRegStr HKCU "Software\$app_reg_path" "DatabaseFilePath" "$data_dir_path\data.sqlite"
  ReadRegStr $0 HKCU "Software\$app_reg_path" "UseSQLiteDB"
  ${If} $0 == ""
    WriteRegStr HKCU "Software\$app_reg_path" "UseSQLiteDB" "True"
    WriteRegStr HKCU "Software\$app_reg_path" "RemoteDBKind" "postgresql"
    WriteRegStr HKCU "Software\$app_reg_path" "RemoteDBHost" "localhost"
    WriteRegStr HKCU "Software\$app_reg_path" "RemoteDBPort" "5432"
    WriteRegStr HKCU "Software\$app_reg_path" "RemoteDBUser" "rpk"
    WriteRegStr HKCU "Software\$app_reg_path" "RemoteDBPassword" "code00"
    WriteRegStr HKCU "Software\$app_reg_path" "RemoteDBName" "teilnehmer"
    WriteRegStr HKCU "Software\$app_reg_path" "DatabaseTable" "participants"
  ${EndIf}
  ReadRegStr $0 HKCU "Software\$app_reg_path" "LastSaveDir"
  ${If} $0 == ""
    WriteRegStr HKCU "Software\$app_reg_path" "LastSaveDir" "$DESKTOP"
  ${EndIf}
SectionEnd

section "uninstall"
  # Always delete uninstaller first
  delete "$install_dir_path\uninstaller.exe"
  delete "$DESKTOP\$app_name.lnk"
 
  RMDir /R $install_dir_path
  RMDir /R $app_menu_path
sectionEnd

!macro DEF_VARS un
  Function ${un}define_vars
    StrCpy $app_name "Teilnehmerbogen"
    StrCpy $app_reg_path "Thelonius\Teilnehmerbogen"
    StrCpy $install_dir_path "$LOCALAPPDATA\$app_name"
    StrCpy $data_dir_path "$APPDATA\$app_name"
    StrCpy $app_exe_path "$install_dir_path\teilnehmerbogen.exe"
    StrCpy $app_menu_path "$STARTMENU\$app_name"
  FunctionEnd
!macroend
 
!insertmacro DEF_VARS ""
!insertmacro DEF_VARS "un."

Function .onInit
  Call define_vars
  MessageBox MB_YESNO "Installation von '$app_name'. Fortfahren?" IDYES NoAbort
    Abort ; causes installer to quit.
  NoAbort:
FunctionEnd

Function un.onInit
  Call un.define_vars
  MessageBox MB_YESNO "Entfernen von '$app_name' und aller dazu gehoerenden Dateien. Fortfahren?" IDYES NoAbort
    Abort
  NoAbort:
FunctionEnd

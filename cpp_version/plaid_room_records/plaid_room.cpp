#include "plaid_room.h"
#include "ui_plaid_room.h"
#include <iostream>

plaid_room::plaid_room(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::plaid_room)
{
    ui->setupUi(this);
    connect(ui->tab_one_search_upc_button,SIGNAL(clicked()),this,SLOT(search_for_upc()));
    connect(ui->tab_one_search_upc_qline,SIGNAL(returnPressed()),this,SLOT(search_for_upc()));
}

void plaid_room::search_for_upc(){
    //call to discogs API
    this->print_to_console("Searching discogs...");
}

void plaid_room::print_to_console(QString str){
    QString text= ui->tab_one_text_browser->toPlainText();
    ui->tab_one_text_browser->setPlainText(text + str);
    ui->tab_one_text_browser->moveCursor(QTextCursor::End);
}

plaid_room::~plaid_room()
{
    delete ui;
}

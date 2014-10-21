#include "plaid_room.h"
#include "ui_plaid_room.h"

plaid_room::plaid_room(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::plaid_room)
{
    ui->setupUi(this);
}

plaid_room::~plaid_room()
{
    delete ui;
}

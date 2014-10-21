#include "mainwindow.h"
#include <QApplication>
#include "plaid_room.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    //MainWindow w;
    //w.show();
    plaid_room p;
    p.show();

    return a.exec();
}

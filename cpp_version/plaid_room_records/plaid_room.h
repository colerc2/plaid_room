#ifndef PLAID_ROOM_H
#define PLAID_ROOM_H

#include <QWidget>

namespace Ui {
class plaid_room;
}

class plaid_room : public QWidget
{
    Q_OBJECT

public:
    explicit plaid_room(QWidget *parent = 0);
    ~plaid_room();

private:
    Ui::plaid_room *ui;
};

#endif // PLAID_ROOM_H

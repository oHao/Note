### 开始
本章节依次讲解了Netty的核心组成部分，并包含简单的例子让你可以快速上手。在本章结束之后，你可以写出依赖Netty的客户端和服务端。
### 准备
如果想要运行本章节的例子，那么最少需要最新版本的Netty和1.6以上的JDK。最新的Netty请到http://netty.io/downloads.html 下载，JDK请自行下载(建议官方)
如果你对本章节中介绍的类有疑问，请查阅官方API文档。另外，如果在使用过程中有任何问题，任何建议，请告知http://netty.io/community.html
### 编写一个Discard服务
最简单的协议不是'Hello,world!',而是DISCARD。DISCARD协议会将所有收到的数据丢弃，也不做任何响应（简单来说，就是什么都不做）
为了实现这个DISCARD协议，你只需要忽略所有的收到的数据就好了。让我们直接从编写一个处理Netty产生的I/O事件类开始。
```java
public class DiscardServerHandler extends ChannelInboundHandlerAdapter{

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        //DISCARD就是这样，把数据偷偷扔掉
        ((ByteBuf)msg).release();
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        //抛出异常时关闭链接
        cause.printStackTrace();
        ctx.close();
    }
}
```
1. DiscardServerHandler 继承自ChannelInboundHandlerAdapter，而ChannelInboundHandlerAdapter是ChannelInboundHandler的一个实现。ChannelInboundHandler提供了很多可以重写的方法。但是现在继承ChannelInboundHandlerAdapter就够了，不必要去实现ChannelInboundHandler。
1. 我们重写了channelRead()这个方法。这个方法是在接收完数据时调用的，例子中接收数据的数据类型是ByteBuf。
1. 为了实现这个DISCARD协议，方法中忽略了接收到的数据。ByteBuf 是一种引用计数的对象，并且它必须显式的用releaser()方法释放。请记住：每一个经过handler的引用计数的对象都应该由handler释放。所以，channelRead()通常以以下形式实现：
```java
  这是示例代码
        try {
            //自己的逻辑

        }
        finally {
		//无论如何，都要释放掉。
            ReferenceCountUtil.release(msg);
        }
```
1. exceptionCaught() 事件处理方法是在Netyy抛出I/O错误或者实现的handler方法上抛出异常时调用。在大多数情况，捕获的异常应该被打印出来，并且将相关的Channel关闭。但是，当你想在发生异常时做一些处理，重写这个方法会给你带来不同的思路。比如，在关闭连接前，发送错误码作为回应。

一切OK。我门已经实现了这个DISCARD服务器的第一部分，下一步就是写一个main()方法来启动一个使用DiscardServerHandler的服务器。
```java
public class DiscardServer {
    private int port;
    public DiscardServer(int port){
        this.port = port;
    }
    public void run(){
        EventLoopGroup bossGroup = new NioEventLoopGroup();
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        try{
            ServerBootstrap sb = new ServerBootstrap();
            sb.group(bossGroup,workerGroup).channel(NioServerSocketChannel.class)
                    .childHandler(new ChannelInitializer<SocketChannel>() {
                        protected void initChannel(SocketChannel socketChannel) throws Exception {
                            socketChannel.pipeline().addLast(new DiscardServerHandler());
                        }
                    })
                    .option(ChannelOption.SO_BACKLOG,128)
                    .childOption(ChannelOption.SO_KEEPALIVE,true);
            ChannelFuture f = sb.bind(port).sync();
            f.channel().closeFuture().sync();
        }
        catch (Exception e){
            e.printStackTrace();
        }
        finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
    public static void main(String[] args) throws Exception {
        int port;
        if (args.length > 0) {
            port = Integer.parseInt(args[0]);
        } else {
            port = 8080;
        }
        new DiscardServer(port).run();
    }
```
2. NioEventLoopGroup是一个处理I/O操作的多线程事件循环。Netty为不同类型的传输模式提供了各种EventLoopGroup实现。我门实现了一个服务器端的应用，并且，在这个例子里用到了两个NioEventLoopGroup。第一个，经常被称为“boss”，接收一个即将到达的连接。第二个，被称为“worker”，在boss接收一个连接并且在其上注册之后处理在该连接上的数据。使用多少个线程，这些线程如何映射到Channel(通道)上取决于对EventLoopGroup的具体实现，或者通过构造器配置。
2. ServerBootstrap 是一个建立服务的帮助类。你也可以使用Channel直接建立服务。无论如何，请记住这是一个枯燥的过程，而且在大多数情况下并不需要这么做。
2. 我们指定使用NioServerSocketChannel类，该类用于实例化一个新通道来接收传入连接。
2. ChannelInitializer始终由新接收的Channel来评估。ChannelInitializer是为了帮助用户配置一个新的Channel而生的handler。您很可能希望通过添加一些处理程序(例如DiscardServerHandler)来配置新通道的通道管道，以实现您的网络应用程序。随着程序变得复杂，可以给pipeline加入更多的handler类，最终将这个匿名类抽取到外部类中。
2. 你也可以在Channel实现类设置参数。现在我们正在写一个TCP/IP 服务，所以我们可以设置像tcpNoDelay 和 keepAlive这样的设置。详细的设置请参照官方文档关于ChannelOption和ChannelConfig的部分。
2. option()是对接收连接的NioServerSocketChannel，而childOption()是用于父通道接受的通道，在本例中为NioServerSocketChannel。
2. 剩下的是绑定到端口并启动服务器。在这里，我们绑定到机器上所有NICs(网络接口卡)的端口8080。现在可以任意多次调用bind()方法(使用不同的绑定地址)。

### 运行
修改DiscardServerHandler类如下所示：
```java
public class DiscardServerHandler extends ChannelInboundHandlerAdapter{

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
//  这是示例代码
//        try {
//            //DISCARD就是这样，把数据偷偷扔掉
//
//        }
//        finally {
//            ReferenceCountUtil.release(msg);
//        }
        ByteBuf in = (ByteBuf) msg;
        try {
            while (in.isReadable()) { // (1)
                System.out.print((char) in.readByte());
                System.out.flush();
            }
        } finally {
            ReferenceCountUtil.release(msg); // (2)
        }
    }
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        //抛出异常时关闭链接
        cause.printStackTrace();
        ctx.close();
    }
}
```
其实只是做了打印接收到的信息而已。打开浏览器，输入localhost:8080，就可以在控制台看见请求头信息了。

















## Echo和Time服务
#### Echo
在上一节中，我们实现了一个丢弃所有数据的DISCARD服务，但是一个服务通常来说都会对请求进行响应。现在让我们开始写一个Echo服务--返回收到的数据，来学习如何写入响应信息。
DISCARD和Echo唯一不同的地方时DISCARD是将收到的数据打印到控制台当中，而Echo是将数据返回。所以只需要对DISCARD中的channelRead()稍作修改即可。
```java
 @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        ctx.write(msg); // (1)
        ctx.flush(); // (2)
    }
```
1. ChannelHandlerContext 对象提供了多种操作，可以让我们来出发各种I/O事件和操作。在这，我们执行了writer(object)将收到的数据写进去。请注意，在这里我们没有释放数据对像--这是因为Netty会自动释放写出的对象。
1. ctx.write(msg)这行代码并没有确保数据已经写出--数据被缓存在里面，在调用ctx.flush()之后数据才被‘冲刷’出去。另外，ctx.writeAndFlush(msg)是另一种更简洁的方案。
修改完成之后，运行程序，访问本地的服务，你就能看到结果了。
#### Time
接下来我们要说的是一个Time服务。和前面两个例子不同的是，Time服务在不接受请求的情况下，发送一个32位整数，并且在信息发送完成后关闭连接。在这个例子里，会学到如何去构造和发送信息，并在完成时关闭连接。
因为我们会忽略所有收到的信息，并在连接建立时发送信息，所以在这里ChannelRead()方法不再适用了。下面我们介绍ChannelActive()方法。代码如下：
```java
public class TimeServerHandler extends ChannelInboundHandlerAdapter {

    @Override
    public void channelActive(final ChannelHandlerContext ctx) { // (1)
        final ByteBuf time = ctx.alloc().buffer(4); // (2)
        time.writeInt((int) (System.currentTimeMillis() / 1000L + 2208988800L));
        
        final ChannelFuture f = ctx.writeAndFlush(time); // (3)
        f.addListener(new ChannelFutureListener() {
            @Override
            public void operationComplete(ChannelFuture future) {
                assert f == future;
                ctx.close();
            }
        }); // (4)
    }
    
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        cause.printStackTrace();
        ctx.close();
    }
}
```
2. channelActive() 方法在连接建立完成时调用。数据就是在这个方法里写入的。
2. 在发送信息之前，我们先要建造一个用来存放信息的缓存。因为我门要发送的是32位的整数，所以需要一个至少4字节的ByteBuf，通过ctx对象可以获取到当前的ByteBufAllocator对象--它可以给你新的缓存区。
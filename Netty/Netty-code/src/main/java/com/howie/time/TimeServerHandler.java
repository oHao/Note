package com.howie.time;

import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelFutureListener;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;

public class TimeServerHandler extends ChannelInboundHandlerAdapter{
    @Override
    public void channelActive(final ChannelHandlerContext ctx) throws Exception {
        ByteBuf time = ctx.alloc().buffer(32);
        String l = String.valueOf(System.currentTimeMillis());
        time.writeBytes(l.getBytes());
        ChannelFuture f = ctx.writeAndFlush(time);
        f.addListener(new ChannelFutureListener() {
            public void operationComplete(ChannelFuture channelFuture) throws Exception {
                ctx.close();
            }
        });
    }
}
